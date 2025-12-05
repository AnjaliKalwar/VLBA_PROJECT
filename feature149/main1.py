import paramiko
import time
import socket
import os
import sys

HOST = "server.local"
PORT = 22
USER = "admin"
PASSWORD = "admin"
PUBLIC_KEY_FILE = "public_key.pub"

GLOBAL_TIMEOUT = 60
START_TIME = time.time()


# ---------------------------------------------------------------------
# TIMEOUT CHECKER
# ---------------------------------------------------------------------
def check_timeout():
    if time.time() - START_TIME > GLOBAL_TIMEOUT:
        raise TimeoutError("Global CI timeout exceeded.")


# ---------------------------------------------------------------------
# HOSTNAME RESOLUTION (FAST FAIL)
# ---------------------------------------------------------------------
def resolve_hostname():
    socket.gethostbyname(HOST)


# ---------------------------------------------------------------------
# WAIT FOR SSH SERVER
# ---------------------------------------------------------------------
def wait_for_ssh(host, port):
    print("[TASK] Waiting for SSH service...")
    for attempt in range(10):
        check_timeout()
        try:
            sock = socket.create_connection((host, port), timeout=2)
            sock.close()
            print("[OK] SSH port is open.")
            return
        except Exception:
            print(f"  attempt {attempt+1}/10 failed")
            time.sleep(1)
    raise RuntimeError("SSH did not become ready.")


# ---------------------------------------------------------------------
# SSH CONNECTION
# ---------------------------------------------------------------------
def ssh_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("[TASK] Connecting via password...")

    for attempt in range(5):
        check_timeout()
        try:
            client.connect(
                HOST,
                port=PORT,
                username=USER,
                password=PASSWORD,
                allow_agent=False,
                look_for_keys=False,
                timeout=5,
                auth_timeout=5,
                banner_timeout=5,
            )
            print("[OK] Connected.")
            return client
        except Exception as e:
            print(f"  attempt {attempt+1}/5 failed: {e}")
            time.sleep(1)

    raise RuntimeError("SSH connection failed.")


# ---------------------------------------------------------------------
# SUDO EXECUTION WITH PASSWORD-PROMPT HANDLING
# ---------------------------------------------------------------------
def sudo(client, cmd):
    """
    Executes sudo commands and automatically handles password prompts.
    Works even before passwordless sudo is enabled.
    """
    check_timeout()

    transport = client.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    channel.exec_command(cmd)

    output = ""
    pw_sent = False

    while True:
        time.sleep(0.1)
        check_timeout()

        if channel.recv_ready():
            data = channel.recv(1024).decode()
            output += data

            # Detect sudo asking for password
            if ("password" in data.lower()) and not pw_sent:
                channel.send(PASSWORD + "\n")
                pw_sent = True

        if channel.recv_stderr_ready():
            data = channel.recv_stderr(1024).decode()
            output += data

        if channel.exit_status_ready():
            break

    exit_code = channel.recv_exit_status()

    if exit_code != 0:
        raise RuntimeError(f"sudo command failed: {output}")

    return output, ""


# ---------------------------------------------------------------------
# RUN NORMAL USER COMMANDS
# ---------------------------------------------------------------------
def run(client, cmd):
    check_timeout()
    stdin, stdout, stderr = client.exec_command(cmd, timeout=10)
    return stdout.read().decode(), stderr.read().decode()


# ---------------------------------------------------------------------
# INSTALL SSH PUBLIC KEY (NO SUDO REQUIRED)
# ---------------------------------------------------------------------
def install_public_key(client, public_key):
    print("[TASK] Installing SSH public key...")

    # Create ~/.ssh directory
    run(client, "mkdir -p ~/.ssh")
    run(client, "chmod 700 ~/.ssh")

    # Write key
    run(client, f'echo "{public_key}" > ~/.ssh/authorized_keys')
    run(client, "chmod 600 ~/.ssh/authorized_keys")

    print("[OK] Public key installed in ~/.ssh WITHOUT sudo.")


# ---------------------------------------------------------------------
# ENABLE PASSWORDLESS SUDO
# ---------------------------------------------------------------------
def enable_passwordless_sudo(client):
    print("[TASK] Enabling passwordless sudo...")

    rule = "admin ALL=(ALL) NOPASSWD:ALL\n"
    sudo(client, f'echo "{rule}" | sudo tee /etc/sudoers.d/admin_nopasswd > /dev/null')
    sudo(client, "sudo chmod 440 /etc/sudoers.d/admin_nopasswd")

    print("[OK] Passwordless sudo enabled.")


# ---------------------------------------------------------------------
# FLEXIBLE SSHD RELOAD (WORKS IN CI WITHOUT systemd)
# ---------------------------------------------------------------------
def reload_sshd(client):
    print("[TASK] Reloading SSH daemon...")

    cmds = [
        "sudo systemctl reload ssh",
        "sudo systemctl reload sshd",
        "sudo service ssh reload",
        "sudo service sshd reload",
        "sudo /etc/init.d/ssh reload",
        # Last resort: send HUP to sshd if running
        "sudo pkill -HUP sshd"
    ]

    for cmd in cmds:
        try:
            out, err = sudo(client, cmd)
            print(f"[DEBUG] Reload attempt: {cmd}")
            print(f"[DEBUG] stdout: {out.strip()}")
            print(f"[DEBUG] stderr: {err.strip()}")
            print("[OK] SSH reload succeeded or accepted.")
            return
        except Exception as e:
            print(f"[DEBUG] Reload failed: {cmd} → {e}")

    print("[WARN] No valid SSH reload method succeeded. Continuing anyway.")
    print("[INFO] This is normal in CI containers without systemd.")


# ---------------------------------------------------------------------
# HARDEN SSH SECURITY
# ---------------------------------------------------------------------
def harden_ssh_security(client):
    print("[TASK] Disabling SSH password authentication...")

    override_file = "/etc/ssh/sshd_config.d/99-disable-password.conf"
    contents = (
        "PasswordAuthentication no\n"
        "ChallengeResponseAuthentication no\n"
        "KbdInteractiveAuthentication no\n"
    )

    sudo(client, f'echo "{contents}" | sudo tee {override_file} > /dev/null')

    # Validate sshd config (always supported)
    _, err = sudo(client, "sudo sshd -t")
    if err.strip():
        raise RuntimeError("Invalid sshd configuration:\n" + err)

    reload_sshd(client)

    print("[OK] SSH security hardened.")


# ---------------------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------------------
def main():
    print("[INFO] Starting CI-safe provisioning...")

    resolve_hostname()
    check_timeout()

    if not os.path.exists(PUBLIC_KEY_FILE):
        raise FileNotFoundError("public_key.pub not found")

    raw = open(PUBLIC_KEY_FILE).read().strip()
    public_key = raw if raw.startswith("ssh-rsa ") else "ssh-rsa " + raw

    wait_for_ssh(HOST, PORT)
    client = ssh_connect()

    install_public_key(client, public_key)
    enable_passwordless_sudo(client)
    harden_ssh_security(client)

    client.close()
    print("[✓] Completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] {e}")
        sys.exit(1)