#!/usr/bin/env python3
import paramiko
import time
import os

# -----------------------------
# CONFIG
# -----------------------------
HOST = "server.local"
PORT = 22
USER = "admin"
PASSWORD = "admin"
PUBLIC_KEY_FILE = "public_key.pub"

# -----------------------------
# HELPERS
# -----------------------------
def sudo(ssh, cmd):
    """
    Run a sudo command non-interactively by sending password using -S.
    This FIXES the 'sudo: a terminal is required' error.
    """
    full = f'echo "{PASSWORD}" | sudo -S sh -c "{cmd}"'
    stdin, stdout, stderr = ssh.exec_command(full)
    time.sleep(0.25)
    return stdout.read(), stderr.read()


def wait_for_server(ssh):
    for _ in range(20):
        try:
            ssh.exec_command("echo ok")
            return
        except Exception:
            time.sleep(1)

# -----------------------------
# MAIN
# -----------------------------
def main():
    # 1. Validate key presence
    if not os.path.exists(PUBLIC_KEY_FILE):
        print(f"[!] Missing key: {PUBLIC_KEY_FILE}")
        return

    with open(PUBLIC_KEY_FILE, "r") as f:
        public_key = f.read().strip()

    # Ensure correct prefix
    if not public_key.startswith("ssh-"):
        public_key = "ssh-rsa " + public_key

    # 2. SSH login (password)
    print("[+] Connecting to server...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        HOST, port=PORT,
        username=USER,
        password=PASSWORD,
        look_for_keys=False,
        allow_agent=False
    )
    wait_for_server(ssh)

    # 3. Install authorized_keys
    print("[+] Installing SSH key...")
    cmds = [
        "mkdir -p ~/.ssh",
        "chmod 700 ~/.ssh",
        f'echo "{public_key}" > ~/.ssh/authorized_keys',
        "chmod 600 ~/.ssh/authorized_keys",
    ]
    for c in cmds:
        ssh.exec_command(c)
        time.sleep(0.15)

    # 4. Passwordless sudo
    print("[+] Setting passwordless sudo...")

    sudo(ssh, 'echo "admin ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/admin')
    sudo(ssh, "chmod 440 /etc/sudoers.d/admin")

    # 5. Disable password-based SSH login
    print("[+] Disabling password SSH login...")

    sudo(ssh, "cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")

    sudo(ssh, 'sed -i "s/^PasswordAuthentication.*/PasswordAuthentication no/" /etc/ssh/sshd_config')
    sudo(ssh, 'sed -i "s/^#PasswordAuthentication.*/PasswordAuthentication no/" /etc/ssh/sshd_config')

    # 6. Restart SSH
    print("[+] Restarting SSH daemon...")
    sudo(ssh, "systemctl reload sshd || service ssh restart")

    print("\n[✓] ALL DONE — passwordless sudo + key auth enabled.\n")

    ssh.close()


if __name__ == "__main__":
    main()
