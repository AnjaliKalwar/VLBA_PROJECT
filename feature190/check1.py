#!/usr/bin/env python3
import subprocess
import requests
import os

API_URL = os.environ.get("API_URL", "http://localhost:5003")


USERNAME = "vlba_anjali_kalwar1"
PASSWORD = "anjali070700"

DB_USER = "app_user"
DB_PASS = "app_password"
DB_NAME = "login_db"

DB1_CONTAINER = "db1"
DB2_CONTAINER = "db2"


def show_db_state(db_container):
    print(f"\n\n Database state in {db_container}:")

    mysql_cmd = (
        "USE login_db; "
        "SHOW TABLES; "
        "SELECT * FROM users; "
        "SELECT * FROM sessions;"
    )

    subprocess.run([
        "docker", "exec", "-i", db_container,
        "mysql",
        f"-u{DB_USER}",
        f"-p{DB_PASS}",
        "-e",
        mysql_cmd
    ])


# -----------------------------
# Step 1: create_login
# -----------------------------
print("\n ##########Creating user...##########")
resp = requests.post(
    f"{API_URL}/create_login",
    json={"username": USERNAME, "password": PASSWORD}
)

if resp.status_code == 200:
    print(f"----->>::User '{USERNAME}' created::<<-----")
elif resp.status_code == 400:
    print(f"----->>:: User '{USERNAME}' already exists:<<-----")
else:
    print("----->>:: create_login failed:<<-----")
    exit(1)

# -----------------------------
# Step 2: login
# -----------------------------
print("\n\n########## Logging in...##########")
resp = requests.post(
    f"{API_URL}/login",
    json={"username": USERNAME, "password": PASSWORD}
)

if resp.status_code != 200:
    print("----->>:: Login failed")
    exit(1)

session_id = resp.json()["session_id"]
print(f"----->>:: Login successful, session_id={session_id}:<<-----")

# -----------------------------
# Step 3: Show DB state after login
# -----------------------------
show_db_state(DB1_CONTAINER)
show_db_state(DB2_CONTAINER)

# -----------------------------
# Step 4: logout
# -----------------------------
print("\n\n########## Logging out...##########")
resp = requests.post(
    f"{API_URL}/logout",
    params={"session_id": session_id}
)

if resp.status_code != 200:
    print("----->>:: Logout failed:<<-----")
    exit(1)

print(f"----->>:: Logout successful for session_id={session_id}:<<-----")

# -----------------------------
# Step 5: Show DB state after logout
# -----------------------------
show_db_state(DB1_CONTAINER)
show_db_state(DB2_CONTAINER)

print("\n CHECK COMPLETED SUCCESSFULLY")
