import paramiko
import time
import os
# -----------------------------
# CONFIGURATION
# -----------------------------
HOST = "server.local"         # Use Docker-mapped host
PORT = 22               # Mapped container SSH port
USER = "admin"
PASSWORD = "admin"
PUBLIC_KEY_FILE = "public_key.pub"  # Path to public key
# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def wait_for_server(ssh):
    """Wait a moment if SSH service is not ready."""
    for _ in range(10):
        try:
            ssh.exec_command("echo ok")
            return
        except Exception:
            time.sleep(1)
# -----------------------------
# MAIN SCRIPT
# -----------------------------
def main():
    # 1. Check public key file
    if not os.path.exists(PUBLIC_KEY_FILE):
        print(f"[!] Public key file '{PUBLIC_KEY_FILE}' not found")
        return
    with open(PUBLIC_KEY_FILE, "r") as f:
        raw_key = f.read().strip()
    # Ensure proper SSH public key format
    if not raw_key.startswith("ssh-rsa "):
        public_key = "ssh-rsa " + raw_key
    else:
        public_key = raw_key
    # 2. Connect via password
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("[+] Connecting via password ...")
    try:
        ssh.connect(
            HOST,
            port=PORT,
            username=USER,
            password=PASSWORD,
            look_for_keys=False,
            allow_agent=False
        )
    except Exception as e:
        print(f"[!] SSH connection failed: {e}")
        return
    wait_for_server(ssh)
    # 3. Create .ssh folder and upload public key
    print("[+] Installing public key ...")
    commands = [
        "mkdir -p ~/.ssh",
        "chmod 700 ~/.ssh",
        f'echo "{public_key}" > ~/.ssh/authorized_keys',
        "chmod 600 ~/.ssh/authorized_keys"
    ]
    for cmd in commands:
        ssh.exec_command(cmd)
        time.sleep(0.2)
    # 4. Enable passwordless sudo for admin
    print("[+] Enabling passwordless sudo ...")
    sudo_rule = "admin ALL=(ALL) NOPASSWD:ALL\n"
    ssh.exec_command(
        f'echo "{sudo_rule}" | sudo tee /etc/sudoers.d/admin_nopasswd > /dev/null',
        get_pty=True
    )
    time.sleep(0.5)
    # 5. Disable SSH password login
    print("[+] Disabling password login in SSH ...")
    ssh.exec_command("sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak", get_pty=True)
    time.sleep(0.3)
    ssh.exec_command(
        'sudo sed -i "s/^PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config',
        get_pty=True
    )
    ssh.exec_command(
        'sudo sed -i "s/^#PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config',
        get_pty=True
    )
    time.sleep(0.3)
    # 6. Reload SSH
    print("[+] Reloading SSH service ...")
    ssh.exec_command("sudo systemctl reload sshd || sudo service ssh restart", get_pty=True)
    time.sleep(1)
    print("[✓] Setup completed successfully.")
    ssh.close()
# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    main()