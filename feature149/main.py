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
def wait_for_server(ssh):
    """Wait until the SSH daemon is fully ready."""
    for _ in range(20):
        try:
            ssh.exec_command("echo ok")
            return
        except Exception:
            time.sleep(1)

def run_as_root(ssh, command):
    """
    Execute command as root WITHOUT sudo (sudo requires interactive TTY).
    Use: echo password | su -c "<command>"
    """
    su_cmd = f'echo "{PASSWORD}" | su -c "{command}"'
    ssh.exec_command(su_cmd)
    time.sleep(0.3)

# -----------------------------
# MAIN
# -----------------------------
def main():

    # 1. Load public key
    if not os.path.exists(PUBLIC_KEY_FILE):
        print(f"[!] Public key file '{PUBLIC_KEY_FILE}' not found")
        return

    with open(PUBLIC_KEY_FILE, "r") as f:
        raw_key = f.read().strip()

    # Ensure correct OpenSSH format
    if not raw_key.startswith("ssh-rsa "):
        public_key = "ssh-rsa " + raw_key
    else:
        public_key = raw_key

    # 2. Connect using password
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("[+] Connecting with password ...")
    ssh.connect(
        HOST,
        port=PORT,
        username=USER,
        password=PASSWORD,
        look_for_keys=False,
        allow_agent=False
    )

    wait_for_server(ssh)

    # 3. Install public key
    print("[+] Installing authorized_keys ...")
    commands = [
        "mkdir -p ~/.ssh",
        "chmod 700 ~/.ssh",
        f'echo "{public_key}" > ~/.ssh/authorized_keys',
        "chmod 600 ~/.ssh/authorized_keys",
    ]
    for cmd in commands:
        ssh.exec_command(cmd)
        time.sleep(0.2)

    # 4. Set up passwordless sudo for admin
    print("[+] Setting passwordless sudo ...")

    run_as_root(ssh, 'echo "admin ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/admin_nopasswd')
    run_as_root(ssh, "chmod 440 /etc/sudoers.d/admin_nopasswd")

    # 5. Disable password-based SSH login
    print("[+] Disabling SSH password login ...")

    run_as_root(ssh, "cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")

    run_as_root(ssh, 'sed -i "s/^PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config')
    run_as_root(ssh, 'sed -i "s/^#PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config')

    # 6. Reload SSH
    print("[+] Reloading SSH service ...")
    run_as_root(ssh, "systemctl reload sshd || service ssh restart")

    print("[✓] Setup completed successfully.")
    ssh.close()


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()
