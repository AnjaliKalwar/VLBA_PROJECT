import paramiko
import time
import os

HOST = "server.local"
PORT = 22
USER = "admin"
PASSWORD = "admin"
PUBLIC_KEY_FILE = "public_key.pub"

def run_sudo(ssh, cmd):
    """
    Execute sudo command while providing password via stdin.
    """
    stdin, stdout, stderr = ssh.exec_command("sudo -S -p '' " + cmd, get_pty=True)
    stdin.write(PASSWORD + "\n")
    stdin.flush()
    return stdout.read().decode(), stderr.read().decode()


def wait_for_server(ssh):
    for _ in range(10):
        try:
            ssh.exec_command("echo ok")
            return
        except Exception:
            time.sleep(1)


def main():
    if not os.path.exists(PUBLIC_KEY_FILE):
        print(f"[!] Missing public key: {PUBLIC_KEY_FILE}")
        return

    with open(PUBLIC_KEY_FILE, "r") as f:
        raw_key = f.read().strip()

    if not raw_key.startswith("ssh-rsa "):
        public_key = "ssh-rsa " + raw_key
    else:
        public_key = raw_key

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("[+] Connecting via password ...")
    ssh.connect(
        HOST,
        port=PORT,
        username=USER,
        password=PASSWORD,
        look_for_keys=False,
        allow_agent=False
    )

    wait_for_server(ssh)

    # Install public key
    ssh.exec_command("mkdir -p ~/.ssh && chmod 700 ~/.ssh")
    ssh.exec_command(f'echo "{public_key}" > ~/.ssh/authorized_keys')
    ssh.exec_command("chmod 600 ~/.ssh/authorized_keys")

    # --- FIX: correct passwordless sudo setup ---
    print("[+] Enabling passwordless sudo ...")
    sudo_rule = "admin ALL=(ALL) NOPASSWD:ALL\n"
    run_sudo(ssh, f'echo "{sudo_rule}" > /etc/sudoers.d/admin_nopasswd')
    run_sudo(ssh, "chmod 440 /etc/sudoers.d/admin_nopasswd")

    # Disable password login
    print("[+] Disabling password login ...")
    run_sudo(ssh, "cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")
    run_sudo(ssh, 'sed -i "s/^PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config')
    run_sudo(ssh, 'sed -i "s/^#PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config')

    print("[+] Reloading SSH ...")
    run_sudo(ssh, "systemctl reload sshd || service ssh restart")

    print("[✓] Setup completed successfully.")
    ssh.close()


if __name__ == "__main__":
    main()
