#!/usr/bin/env python3

import paramiko
import socket
import time
import os
import sys

# CONFIGURATION
SSH_HOST = "server.local"       
SSH_PORT = 22
SSH_USER = "admin"
SSH_PASS = "admin"
SSH_PUBLIC_KEY_FILE = "public_key.pub"

SCRIPT_TIMEOUT = 60
SCRIPT_START_TIME = time.time()

# HELPER FUNCTIONS
def check_script_timeout():
    if time.time() - SCRIPT_START_TIME > SCRIPT_TIMEOUT:
        raise TimeoutError("Global CI timeout exceeded")
    print("Checked script timeout")

def wait_for_ssh_port(host, port, retries=10):
    print("Checking if SSH service is available...")
    for attempt in range(1, retries + 1):
        check_script_timeout()
        try:
            sock = socket.create_connection((host, port), timeout=2)
            sock.close()
            print(f"SSH port {port} is open on {host}, attempt {attempt}")
            return
        except Exception:
            print(f"SSH port not open yet, attempt {attempt} of {retries}")
            time.sleep(1)
    raise RuntimeError("SSH did not become ready")

def ssh_connect_with_password(retries=5):
    print(f"Trying to connect to {SSH_HOST} via password authentication...")
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
            print(f"Successfully connected to {SSH_HOST} on attempt {attempt}")
            return ssh_client
        except Exception as e:
            print(f"Connection attempt {attempt} failed: {e}")
            time.sleep(1)
    raise RuntimeError("SSH connection failed")

def run_command(ssh_client, cmd):
    check_script_timeout()
    print(f"Running command: {cmd}")
    stdin, stdout, stderr = ssh_client.exec_command(cmd, timeout=10)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out:
        print(f"Command output:\n{out}")
    if err:
        print(f"Command error:\n{err}")
    return out, err

def sudo_command(ssh_client, cmd):
    check_script_timeout()
    print(f"Running sudo command: {cmd}")
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
                print("Sending sudo password")
                channel.send(SSH_PASS + "\n")
                password_sent = True
        if channel.recv_stderr_ready():
            output += channel.recv_stderr(1024).decode()
        if channel.exit_status_ready():
            break

    exit_code = channel.recv_exit_status()
    if exit_code != 0:
        raise RuntimeError(f"Sudo command failed: {output}")
    print("Sudo command completed successfully")
    return output, ""

def install_ssh_key(ssh_client, public_key):
    print("Creating .ssh directory and setting permissions")
    run_command(ssh_client, "mkdir -p ~/.ssh")
    run_command(ssh_client, "chmod 700 ~/.ssh")
    print("Adding public key to authorized_keys")
    run_command(ssh_client, f'echo "{public_key}" > ~/.ssh/authorized_keys')
    run_command(ssh_client, "chmod 600 ~/.ssh/authorized_keys")
    print("SSH key installation complete")

def enable_sudo_nopasswd(ssh_client):
    print("Configuring passwordless sudo for the admin user")
    rule = "admin ALL=(ALL) NOPASSWD:ALL\n"
    sudo_command(ssh_client, f'echo "{rule}" | sudo tee /etc/sudoers.d/admin_nopasswd > /dev/null')
    sudo_command(ssh_client, "sudo chmod 440 /etc/sudoers.d/admin_nopasswd")
    print("Passwordless sudo configuration complete")

def reload_ssh_service(ssh_client):
    print("Attempting to reload SSH service to apply changes")
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
            if out.strip():
                print(out.strip())
            if err.strip():
                print(err.strip())
            print(f"SSH reload successful using: {cmd}")
            return
        except Exception as e:
            print(f"SSH reload attempt failed: {cmd}, error: {e}")
    print("No SSH reload method succeeded, continuing")

def harden_ssh(ssh_client):
    print("Disabling password authentication for SSH")
    override_file = "/etc/ssh/sshd_config.d/99-disable-password.conf"
    contents = (
        "PasswordAuthentication no\n"
        "ChallengeResponseAuthentication no\n"
        "KbdInteractiveAuthentication no\n"
    )
    sudo_command(ssh_client, f'echo "{contents}" | sudo tee {override_file} > /dev/null')
    _, err = sudo_command(ssh_client, "sudo sshd -t")
    if err.strip():
        raise RuntimeError("Invalid SSH configuration:\n" + err)
    reload_ssh_service(ssh_client)
    print("SSH password authentication disabled and configuration verified")

# MAIN EXECUTION
def main():
    print("Starting SSH key provisioning and security hardening")

    if not os.path.exists(SSH_PUBLIC_KEY_FILE):
        raise FileNotFoundError(f"Public key file {SSH_PUBLIC_KEY_FILE} not found")

    raw_key = open(SSH_PUBLIC_KEY_FILE).read().strip()
    ssh_public_key = raw_key if raw_key.startswith("ssh-rsa ") else "ssh-rsa " + raw_key
    print("Loaded public key from file")

    wait_for_ssh_port(SSH_HOST, SSH_PORT)
    ssh_client = ssh_connect_with_password()

    install_ssh_key(ssh_client, ssh_public_key)
    enable_sudo_nopasswd(ssh_client)
    harden_ssh(ssh_client)

    ssh_client.close()
    print("Provisioning and hardening complete")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Fatal error:", e)
        sys.exit(1)
