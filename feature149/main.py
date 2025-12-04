import paramiko
import os
import time

# -----------------------------
# CONFIGURATION
# -----------------------------
HOST = "server.local"
PORT = 22
USER = "admin"
PASSWORD = "admin"
PUBLIC_KEY_FILE = "public_key.pub"


# -----------------------------
# HELPER
# -----------------------------
def wait_for_server(ssh):
    for _ in range(10):
        try:
            ssh.exec_command("echo ok")
            return
        except Exception:
            time.sleep(1)


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

    if not raw_key.startswith("ssh-rsa "):
        public_key = "ssh-rsa " + raw_key
    else:
        public_key = raw_key

    # 2. Connect using password
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("[+] Connecting to server via password ...")
    ssh.connect(
        HOST,
        port=PORT,
        username=USER,
        password=PASSWORD,
        look_for_keys=False,
        allow_agent=False
    )

    wait_for_server(ssh)

    # 3. Install authorized_keys
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

    # 4. Enable passwordless sudo (WITH PTY)
    print("[+] Enabling passwordless sudo ...")

    sudo_content = "admin ALL=(ALL) NOPASSWD:ALL\n"

    # Write sudoers file as root
    ssh.exec_command(
        f'echo "{sudo_content}" | sudo tee /etc/sudoers.d/admin_nopasswd',
        get_pty=True
    )
    time.sleep(0.5)

    # Fix permissions and ownership WITH PTY
    ssh.exec_command("sudo chmod 440 /etc/sudoers.d/admin_nopasswd", get_pty=True)
    time.sleep(0.3)

    ssh.exec_command("sudo chown root:root /etc/sudoers.d/admin_nopasswd", get_pty=True)
    time.sleep(0.3)

    # 5. Disable password authentication in SSH
    print("[+] Disabling SSH password authentication ...")

    ssh.exec_command(
        "sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak",
        get_pty=True
    )
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
    ssh.exec_command(
        "sudo systemctl reload sshd || sudo service ssh restart",
        get_pty=True
    )
    time.sleep(1)

    print("[✓] Setup completed successfully.")
    ssh.close()


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()
