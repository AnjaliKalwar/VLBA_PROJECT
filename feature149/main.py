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
# HELPER FUNCTIONS
# -----------------------------
def wait_for_server(ssh, retries=10, delay=1.0):
    """Wait until remote side is ready to execute commands."""
    for _ in range(retries):
        try:
            ssh.exec_command("echo ok")
            return
        except Exception:
            time.sleep(delay)

def run_sudo_command(ssh, command):
    """
    Run a sudo command over a real PTY session.
    Ensures it works on systems requiring a TTY.
    """
    chan = ssh.get_transport().open_session()
    chan.get_pty()
    chan.exec_command(command)
    return chan.recv_exit_status()

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main():
    # 1. Load public key
    if not os.path.exists(PUBLIC_KEY_FILE):
        print(f"[!] Public key file '{PUBLIC_KEY_FILE}' not found")
        return

    with open(PUBLIC_KEY_FILE, "r") as f:
        raw_key = f.read().strip()

    # Ensure proper OpenSSH prefix
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

    # 4. Enable passwordless sudo
    print("[+] Enabling passwordless sudo ...")
    sudo_content = 'admin ALL=(ALL) NOPASSWD:ALL\n'
    run_sudo_command(ssh, f'echo "{sudo_content}" | sudo tee /etc/sudoers.d/admin_nopasswd >/dev/null')
    run_sudo_command(ssh, "sudo chmod 440 /etc/sudoers.d/admin_nopasswd")
    run_sudo_command(ssh, "sudo chown root:root /etc/sudoers.d/admin_nopasswd")

    # 5. Disable password authentication in SSH
    print("[+] Disabling SSH password authentication ...")
    run_sudo_command(ssh, "sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")
    run_sudo_command(
        ssh,
        'sudo sed -i "s/^PasswordAuthentication[[:space:]]\\+yes/PasswordAuthentication no/;'
        's/^#PasswordAuthentication[[:space:]]\\+yes/PasswordAuthentication no/" /etc/ssh/sshd_config'
    )

    # 6. Reload SSH service
    print("[+] Reloading SSH service ...")
    run_sudo_command(
        ssh,
        "sudo systemctl reload sshd || sudo systemctl reload ssh || "
        "sudo service ssh reload || sudo service ssh restart"
    )

    print("[✓] Setup completed successfully.")
    ssh.close()

# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    main()
