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
PASSWORD = "admin"  # for sudo

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def wait_for_ssh(ssh):
    for _ in range(15):
        try:
            ssh.exec_command("echo ok")
            return True
        except:
            time.sleep(1)
    return False


def run_sudo(ssh, cmd):
    """Execute a sudo command interactively, send password if prompted."""
    transport = ssh.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    channel.exec_command(cmd)

    password_sent = False
    output = ""
    while not channel.exit_status_ready():
        time.sleep(0.1)
        if channel.recv_ready():
            data = channel.recv(1024).decode()
            output += data
            if "password" in data.lower() and not password_sent:
                channel.send(PASSWORD + "\n")
                password_sent = True
        if channel.recv_stderr_ready():
            output += channel.recv_stderr(1024).decode()
    return output


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
    try:
        ssh.connect(HOST, port=PORT, username=USER, pkey=key, look_for_keys=False, allow_agent=False)
    except Exception as e:
        print(f"[!] SSH connection failed: {e}")
        return

    wait_for_ssh(ssh)

    # 3. Upload public key
    commands = [
        "mkdir -p ~/.ssh",
        "chmod 700 ~/.ssh",
        f'echo "{pubkey}" > ~/.ssh/authorized_keys',
        "chmod 600 ~/.ssh/authorized_keys"
    ]
    for c in commands:
        ssh.exec_command(c)
        time.sleep(0.2)

    # 4. Enable passwordless sudo (interactive)
    sudoers_line = "admin ALL=(ALL) NOPASSWD:ALL\n"
    run_sudo(ssh, f'echo "{sudoers_line}" | sudo tee /etc/sudoers.d/admin_nopasswd > /dev/null')
    run_sudo(ssh, "sudo chmod 440 /etc/sudoers.d/admin_nopasswd")

    print("[✓] Passwordless sudo enabled.")
    ssh.close()
    


# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    main()
