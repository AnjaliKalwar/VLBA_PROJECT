#!/usr/bin/env python3

import paramiko
import socket
import time
import os
import sys

# -----------------------------
# CONFIGURATION
# -----------------------------
HOST = "server.local"      # or "server.local"
PORT = 22             # SSH port
USER = "admin"
PASSWORD = "admin"
PUBLIC_KEY_FILE = "public_key.pub"

GLOBAL_TIMEOUT = 60      # Max runtime in seconds
START_TIME = time.time()

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def check_timeout():
    if time.time() - START_TIME > GLOBAL_TIMEOUT:
        raise TimeoutError("Global CI timeout exceeded.")

def wait_for_ssh(host, port, retries=10):
    print("[TASK] Waiting for SSH service...")
    for attempt in range(1, retries + 1):
        check_timeout()
        try:
            sock = socket.create_connection((host, port), timeout=2)
            sock.close()
            print(f"[OK] SSH port is open (attempt {attempt})")
            return
        except Exception:
            print(f"  attempt {attempt}/{retries} failed")
            time.sleep(1)
    raise RuntimeError("SSH did not become ready.")

def ssh_connect(retries=5):
    print("[TASK] Connecting via password...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for attempt in range(1, retries + 1):
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
                banner_timeout=5
            )
            print(f"[OK] Connected to {HOST} (attempt {attempt})")
            return client
        except Exception as e:
            print(f"  attempt {attempt}/{retries} failed: {e}")
            time.sleep(1)
    raise RuntimeError("SSH connection failed.")

def run(client, cmd):
    check_timeout()
    stdin, stdout, stderr = client.exec_command(cmd, timeout=10)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out:
        print(f"[stdout] {out}")
    if err:
        print(f"[stderr] {err}")
    return out, err

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
            if "password" in data.lower() and not pw_sent:
                channel.send(PASSWORD + "\n")
                pw_sent = True
        if channel.recv_stderr_ready():
            output += channel.recv_stderr(1024).decode()
        if channel.exit_status_ready():
            break

    exit_code = channel.recv_exit_status()
    if exit_code != 0:
        raise RuntimeError(f"sudo command failed: {output}")
    return output, ""

def install_public_key(client, public_key):
    print("[TASK] Installing SSH public key...")
    run(client, "mkdir -p ~/.ssh")
    run(client, "chmod 700 ~/.ssh")
    run(client, f'echo "{public_key}" > ~/.ssh/authorized_keys')
    run(client, "chmod 600 ~/.ssh/authorized_keys")
    print("[OK] Public key installed in ~/.ssh")

def enable_passwordless_sudo(client):
    print("[TASK] Enabling passwordless sudo...")
    rule = "admin ALL=(ALL) NOPASSWD:ALL\n"
    sudo(client, f'echo "{rule}" | sudo tee /etc/sudoers.d/admin_nopasswd > /dev/null')
    sudo(client, "sudo chmod 440 /etc/sudoers.d/admin_nopasswd")
    print("[OK] Passwordless sudo enabled")

def reload_sshd(client):
    print("[TASK] Reloading SSH daemon...")
    cmds = [
        "sudo systemctl reload ssh",
        "sudo systemctl reload sshd",
        "sudo service ssh reload",
        "sudo service sshd reload",
        "sudo /etc/init.d/ssh reload",
        "sudo pkill -HUP sshd"
    ]
    for cmd in cmds:
        try:
            out, err = sudo(client, cmd)
            print(f"[DEBUG] Reload attempt: {cmd}")
            if out.strip():
                print(f"[stdout] {out.strip()}")
            if err.strip():
                print(f"[stderr] {err.strip()}")
            print("[OK] SSH reload accepted")
            return
        except Exception as e:
            print(f"[DEBUG] Reload failed: {cmd} → {e}")
    print("[WARN] No SSH reload method succeeded; continuing anyway")

def harden_ssh_security(client):
    print("[TASK] Disabling SSH password authentication...")
    override_file = "/etc/ssh/sshd_config.d/99-disable-password.conf"
    contents = (
        "PasswordAuthentication no\n"
        "ChallengeResponseAuthentication no\n"
        "KbdInteractiveAuthentication no\n"
    )
    sudo(client, f'echo "{contents}" | sudo tee {override_file} > /dev/null')
    _, err = sudo(client, "sudo sshd -t")
    if err.strip():
        raise RuntimeError("Invalid sshd configuration:\n" + err)
    reload_sshd(client)
    print("[OK] SSH security hardened")

# -----------------------------
# MAIN EXECUTION
# -----------------------------
def main():
    print("[INFO] Starting CI-safe provisioning...")

    if not os.path.exists(PUBLIC_KEY_FILE):
        raise FileNotFoundError(f"{PUBLIC_KEY_FILE} not found")

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
