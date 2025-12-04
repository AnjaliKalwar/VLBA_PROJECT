#!/usr/bin/env python3
import paramiko
import time
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
HOST = "server.local"
PORT = 22
USER = "admin"
PASSWORD = "admin"
PUBLIC_KEY_FILE = "public_key.pub"

# -----------------------------
# HELPERS
# -----------------------------
def wait_for_ssh(ssh):
    """Wait until SSH is ready."""
    for _ in range(15):
        try:
            ssh.exec_command("echo ok")
            return True
        except:
            time.sleep(1)
    return False

# -----------------------------
# MAIN SCRIPT
# -----------------------------
def main():
    # 1. Load public key
    if not os.path.exists(PUBLIC_KEY_FILE):
        print(f"[!] Public key file '{PUBLIC_KEY_FILE}' not found")
        return

    with open(PUBLIC_KEY_FILE, "r") as f:
        public_key = f.read().strip()

    if not public_key.startswith("ssh-"):
        public_key = "ssh-rsa " + public_key

    # 2. Connect via password
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("[+] Connecting to server...")
    try:
        ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD,
                    look_for_keys=False, allow_agent=False)
    except Exception as e:
        print(f"[!] SSH connection failed: {e}")
        return

    wait_for_ssh(ssh)

    # 3. Install public key
    print("[+] Installing SSH key...")
    cmds = [
        "mkdir -p ~/.ssh",
        "chmod 700 ~/.ssh",
        f'echo "{public_key}" > ~/.ssh/authorized_keys',
        "chmod 600 ~/.ssh/authorized_keys"
    ]
    for cmd in cmds:
        ssh.exec_command(cmd)
        time.sleep(0.2)

    # 4. Disable password authentication in SSH
    print("[+] Disabling password SSH login...")
    ssh.exec_command("sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")
    ssh.exec_command('sudo sed -i "s/^PasswordAuthentication.*/PasswordAuthentication no/" /etc/ssh/sshd_config')
    ssh.exec_command('sudo sed -i "s/^#PasswordAuthentication.*/PasswordAuthentication no/" /etc/ssh/sshd_config')

    # 5. Reload SSH
    ssh.exec_command("sudo systemctl reload sshd || sudo service ssh restart")
    time.sleep(1)

    print("[✓] SSH key installed and password login disabled.")
    ssh.close()
    


# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    main()
