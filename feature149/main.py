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
    for i in range(15):
        try:
            ssh.exec_command("echo ok")
            print(f"[DEBUG] SSH ready after {i+1} attempts")
            return True
        except Exception as e:
            print(f"[DEBUG] SSH not ready yet ({i+1}/15): {e}")
            time.sleep(1)
    return False

def run_command(ssh, cmd, debug=True):
    """Run a command and print output for debugging."""
    if debug:
        print(f"[DEBUG] Running: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if debug:
        print(f"[DEBUG] stdout: {out.strip()}")
        print(f"[DEBUG] stderr: {err.strip()}")
    return out, err

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
        run_command(ssh, cmd)

    # 4. Disable password authentication in SSH
    print("[+] Disabling password SSH login...")
    # These commands require sudo
    cmds_sudo = [
        "cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak",
        'sed -i "s/^PasswordAuthentication.*/PasswordAuthentication no/" /etc/ssh/sshd_config',
        'sed -i "s/^#PasswordAuthentication.*/PasswordAuthentication no/" /etc/ssh/sshd_config',
        "systemctl reload sshd || service ssh restart"
    ]
    for cmd in cmds_sudo:
        out, err = run_command(ssh, f"sudo {cmd}")
        if "sudo: a password is required" in err.lower():
            print("[ERROR] Sudo failed. This is expected if admin does not have passwordless sudo.")
            print("[INFO] Passwordless sudo must be configured in the Dockerfile before running this script.")
            break

    print("[✓] SSH key installed. Password login may not be disabled if sudo failed.")
    ssh.close()


# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":
    main()
