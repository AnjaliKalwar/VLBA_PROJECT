#!/usr/bin/env python3

import paramiko
import socket
import time
import os
import sys

# -----------------------------
# CONFIGURATION
# -----------------------------
SSH_HOST = "server.local"       
SSH_PORT = 22
SSH_USER = "admin"
SSH_PASS = "admin"
SSH_PUBLIC_KEY_FILE = "public_key.pub"

SCRIPT_TIMEOUT = 60      # Max runtime in seconds
SCRIPT_START_TIME = time.time()

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def check_script_timeout():
    if time.time() - SCRIPT_START_TIME > SCRIPT_TIMEOUT:
        raise TimeoutError("Global CI timeout exceeded.")

def wait_for_ssh_port(host, port, retries=10):
    print("[TASK] Waiting for SSH service...")
    for attempt in range(1, retries + 1):
        check_script_timeout()
        try:
            sock = socket.create_connection((host, port), timeout=2)
            sock.close()
            print(f"[OK] SSH port is open (attempt {attempt})")
            return
        except Exception:
            print(f"  attempt {attempt}/{retries} failed")
            time.sleep(1)
    raise RuntimeError("SSH did not become ready.")

def ssh_connect_with_password(retries=5):
    print("[TASK] Connecting via password...")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for attempt in range(1, retries + 1):
        check_script_timeout()
        try:
            ssh_client.connect(
                SSH_HOST,
                port=SSH_PORT,
                username=SSH_USER,
                password=SSH_PASS,
                allow_agent=False,
                look_for_keys=False,
                timeout=5,
                auth_timeout=5,
                banner_timeout=5
            )
            print(f"[OK] Connected to {SSH_HOST} (attempt {attempt})")
            return ssh_client
        except Exception as e:
            print(f"  attempt {attempt}/{retries} failed: {e}")
            time.sleep(1)
    raise RuntimeError("SSH connection failed.")

def run_command(ssh_client, cmd):
    check_script_timeout()
    stdin, stdout, stderr = ssh_client.exec_command(cmd, timeout=10)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out:
        print(f"[stdout] {out}")
    if err:
        print(f"[stderr] {err}")
    return out, err

def sudo_command(ssh_client, cmd):
    check_script_timeout()
    transport = ssh_client.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    channel.exec_command(cmd)
    output = ""
    password_sent = False

    while True:
        time.sleep(0.1)
        check_script_timeout()
        if channel.recv_ready():
            data = channel.recv(1024).decode()
            output += data
            if "password" in data.lower() and not password_sent:
                channel.send(SSH_PASS + "\n")
                password_sent = True
        if channel.recv_stderr_ready():
            output += channel.recv_stderr(1024).decode()
        if channel.exit_status_ready():
            break

    exit_code = channel.recv_exit_status()
    if exit_code != 0:
        raise RuntimeError(f"sudo command failed: {output}")
    return output, ""

def install_ssh_key(ssh_client, public_key):
    print("[TASK] Installing SSH public key...")
    run_command(ssh_client, "mkdir -p ~/.ssh")
    run_command(ssh_client, "chmod 700 ~/.ssh")
    run_command(ssh_client, f'echo "{public_key}" > ~/.ssh/authorized_keys')
    run_command(ssh_client, "chmod 600 ~/.ssh/authorized_keys")
    print("[OK] Public key installed in ~/.ssh")

def enable_sudo_nopasswd(ssh_client):
    print("[TASK] Enabling passwordless sudo...")
    rule = "admin ALL=(ALL) NOPASSWD:ALL\n"
    sudo_command(ssh_client, f'echo "{rule}" | sudo tee /etc/sudoers.d/admin_nopasswd > /dev/null')
    sudo_command(ssh_client, "sudo chmod 440 /etc/sudoers.d/admin_nopasswd")
    print("[OK] Passwordless sudo enabled")

def reload_ssh_service(ssh_client):
    print("[TASK] Reloading SSH daemon...")
    commands = [
        "sudo systemctl reload ssh",
        "sudo systemctl reload sshd",
        "sudo service ssh reload",
        "sudo service sshd reload",
        "sudo /etc/init.d/ssh reload",
        "sudo pkill -HUP sshd"
    ]
    for cmd in commands:
        try:
            out, err = sudo_command(ssh_client, cmd)
            print(f"[DEBUG] Reload attempt: {cmd}")
            if out.strip():
                print(f"[stdout] {out.strip()}")
            if err.strip():
                print(f"[stderr] {err.strip()}")
            print("[OK] SSH reload accepted")
            return
        except Exception as e:
            print(f"[DEBUG] Reload failed: {cmd} → {e}")
    print("[WARN] No SSH reload method succeeded; continuing anyway")

def harden_ssh(ssh_client):
    print("[TASK] Disabling SSH password authentication...")
    override_file = "/etc/ssh/sshd_config.d/99-disable-password.conf"
    contents = (
        "PasswordAuthentication no\n"
        "ChallengeResponseAuthentication no\n"
        "KbdInteractiveAuthentication no\n"
    )
    sudo_command(ssh_client, f'echo "{contents}" | sudo tee {override_file} > /dev/null')
    _, err = sudo_command(ssh_client, "sudo sshd -t")
    if err.strip():
        raise RuntimeError("Invalid sshd configuration:\n" + err)
    reload_ssh_service(ssh_client)
    print("[OK] SSH security hardened")

# -----------------------------
# MAIN EXECUTION
# -----------------------------
def main():
    print("[INFO] Starting CI-safe provisioning...")

    if not os.path.exists(SSH_PUBLIC_KEY_FILE):
        raise FileNotFoundError(f"{SSH_PUBLIC_KEY_FILE} not found")

    raw_key = open(SSH_PUBLIC_KEY_FILE).read().strip()
    ssh_public_key = raw_key if raw_key.startswith("ssh-rsa ") else "ssh-rsa " + raw_key

    wait_for_ssh_port(SSH_HOST, SSH_PORT)
    ssh_client = ssh_connect_with_password()

    install_ssh_key(ssh_client, ssh_public_key)
    enable_sudo_nopasswd(ssh_client)
    harden_ssh(ssh_client)

    ssh_client.close()
    print("[✓] Completed successfully.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] {e}")
        sys.exit(1)
