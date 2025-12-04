import paramiko
import time
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
HOST = "server.local"
PORT = 22
USER = "admin"
PUBKEY_FILE = "public_key.pub"
PRIVATE_KEY_FILE = "private_key.pem"
PASSWORD = "admin"  # needed only for sudo

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def wait_until_ssh_ready(ssh):
    for _ in range(15):
        try:
            ssh.exec_command("echo ok")
            return True
        except:
            time.sleep(1)
    return False


def run_command(ssh, command, use_sudo=False):
    if use_sudo:
        command = f"sudo -S bash -c '{command}'"
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    if use_sudo:
        stdin.write(PASSWORD + "\n")
        stdin.flush()
    return stdout.read().decode(), stderr.read().decode()


# -----------------------------
# MAIN SCRIPT
# -----------------------------
def main():
    # 1. Read public key
    if not os.path.exists(PUBKEY_FILE):
        print(f"[!] Public key '{PUBKEY_FILE}' not found")
        return

    pubkey = open(PUBKEY_FILE).read().strip()
    if not pubkey.startswith("ssh-"):
        pubkey = "ssh-rsa " + pubkey

    # 2. Connect via private key
    if not os.path.exists(PRIVATE_KEY_FILE):
        print(f"[!] Private key '{PRIVATE_KEY_FILE}' not found")
        return

    key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_FILE)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("[+] Connecting via private key...")
    try:
        ssh.connect(
            HOST,
            port=PORT,
            username=USER,
            pkey=key,
            look_for_keys=False,
            allow_agent=False
        )
    except Exception as e:
        print(f"[!] SSH connection failed: {e}")
        return

    wait_until_ssh_ready(ssh)

    # 3. Install SSH public key (ensures future key-based login)
    print("[+] Installing SSH public key...")
    commands = [
        "mkdir -p ~/.ssh",
        "chmod 700 ~/.ssh",
        f'echo "{pubkey}" > ~/.ssh/authorized_keys',
        "chmod 600 ~/.ssh/authorized_keys"
    ]
    for cmd in commands:
        run_command(ssh, cmd)

    # 4. Enable passwordless sudo
    print("[+] Enabling passwordless sudo...")
    sudoers_content = "admin ALL=(ALL) NOPASSWD:ALL\n"
    run_command(ssh, f'echo "{sudoers_content}" | sudo tee /etc/sudoers.d/admin_nopasswd > /dev/null', use_sudo=True)
    run_command(ssh, "sudo chmod 440 /etc/sudoers.d/admin_nopasswd", use_sudo=True)

    print("[✓] Passwordless sudo enabled.")
    ssh.close()


# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    main()
