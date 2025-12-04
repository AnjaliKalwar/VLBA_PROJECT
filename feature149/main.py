#!/usr/bin/env python3
"""
CI-safe SSH key auth, passwordless sudo, and SSH hardening script.
Enhanced debug output for pipelines.
"""

import paramiko
import time
import os
import sys

# -----------------------------
# CONFIGURATION
# -----------------------------
HOST = "server.local"         # Use Docker-mapped host
PORT = 22              # Mapped container SSH port
USER = "admin"
PASSWORD = "admin"
PUBLIC_KEY_FILE = "public_key.pub"  # Path to public key

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def wait_for_server(ssh, retries=10):
    """Wait for SSH server to become responsive."""
    for attempt in range(1, retries + 1):
        try:
            ssh.exec_command("echo ok")
            print(f"[+] SSH server is ready (attempt {attempt})")
            return True
        except Exception as e:
            print(f"[!] SSH not ready yet (attempt {attempt}): {e}")
            time.sleep(1)
    return False

def run_cmd(ssh, cmd, sudo=False):
    """Run a command on remote host and capture output."""
    if sudo:
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    else:
        stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out.strip():
        print(f"[stdout] {out.strip()}")
    if err.strip():
        print(f"[stderr] {err.strip()}")
    return out, err

# -----------------------------
# MAIN SCRIPT
# -----------------------------
def main():
    # 1. Check public key file
    if not os.path.exists(PUBLIC_KEY_FILE):
        print(f"[!] Public key file '{PUBLIC_KEY_FILE}' not found")
        sys.exit(1)

    with open(PUBLIC_KEY_FILE, "r") as f:
        raw_key = f.read().strip()

    # Ensure proper SSH public key format
    public_key = raw_key if raw_key.startswith("ssh-rsa") else "ssh-rsa " + raw_key

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
            allow_agent=False,
            timeout=10
        )
    except Exception as e:
        print(f"[!] SSH connection failed: {e}")
        sys.exit(1)

    if not wait_for_server(ssh):
        print("[!] SSH server never became ready. Exiting.")
        sys.exit(1)

    # 3. Create .ssh folder and upload public key
    print("[+] Installing public key ...")
    commands = [
        "mkdir -p ~/.ssh",
        "chmod 700 ~/.ssh",
        f'echo "{public_key}" > ~/.ssh/authorized_keys',
        "chmod 600 ~/.ssh/authorized_keys"
    ]
    for cmd in commands:
        print(f"[+] Running: {cmd}")
        run_cmd(ssh, cmd)

    # 4. Enable passwordless sudo for admin
    print("[+] Enabling passwordless sudo ...")
    sudo_rule = "admin ALL=(ALL) NOPASSWD:ALL"
    run_cmd(ssh, f'echo "{sudo_rule}" | sudo tee /etc/sudoers.d/admin_nopasswd > /dev/null', sudo=True)

    # 5. Disable SSH password login
    print("[+] Disabling SSH password login ...")
    run_cmd(ssh, "sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak", sudo=True)
    run_cmd(ssh, 'sudo sed -i "s/^PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config', sudo=True)
    run_cmd(ssh, 'sudo sed -i "s/^#PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config', sudo=True)

    # 6. Reload SSH service
    print("[+] Reloading SSH service ...")
    run_cmd(ssh, "sudo systemctl reload sshd || sudo service ssh restart", sudo=True)

    print("[✓] Setup completed successfully.")
    ssh.close()

# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    main()
