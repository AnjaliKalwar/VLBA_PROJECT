#!/usr/bin/env python3
import os
import time
import requests
import mysql.connector

# -----------------------------
# Configuration
# -----------------------------
API_URL = os.environ.get("API_URL", "http://nginx:80")

USERNAME = "vlba_anjali_kalwar1"
PASSWORD = "anjali070700"

DB_CONFIG_1 = {
    "host": "db1",
    "user": "app_user",
    "password": "app_password",
    "database": "login_db",
}

DB_CONFIG_2 = {
    "host": "db2",
    "user": "app_user",
    "password": "app_password",
    "database": "login_db",
}

# -----------------------------
# Wait for API (nginx + fastapi)
# -----------------------------
print("Waiting for API to be ready...")
for i in range(20):
    try:
        r = requests.get(API_URL, timeout=2)
        print("API is reachable")
        break
    except Exception as e:
        print(f"API not ready yet ({i+1}/20): {e}")
        time.sleep(2)
else:
    print("API never became ready")
    exit(1)

# -----------------------------
# Helper: print DB tables
# -----------------------------
def print_db_state(db_name, config):
    print(f"\n{db_name} state:")
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()

    commands = [
        "SHOW TABLES;",
        "SELECT * FROM users;",
        "SELECT * FROM sessions;"
    ]

    for cmd in commands:
        print(f"\nSQL> {cmd}")
        cur.execute(cmd)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    cur.close()
    conn.close()

# -----------------------------
# Step 1: create_login (via NGINX)
# -----------------------------
resp = requests.post(
    f"{API_URL}/create_login",
    json={"username": USERNAME, "password": PASSWORD}
)

if resp.status_code == 200:
    print(f"User {USERNAME} created")
elif resp.status_code == 400:
    print(f"User {USERNAME} already exists")
else:
    print("create_login failed")
    print("Status code:", resp.status_code)
    print("Response body:", resp.text)
    exit(1)

# -----------------------------
# Step 2: login (via NGINX)
# -----------------------------
resp = requests.post(
    f"{API_URL}/login",
    json={"username": USERNAME, "password": PASSWORD}
)

if resp.status_code != 200:
    print("Login failed")
    print("Status code:", resp.status_code)
    print("Response body:", resp.text)
    exit(1)

session_id = resp.json()["session_id"]
print(f"Login successful, session_id={session_id}")

# -----------------------------
# Show DB state AFTER login
# -----------------------------
print_db_state("DB1", DB_CONFIG_1)
print_db_state("DB2", DB_CONFIG_2)

# -----------------------------
# Step 3: logout (via NGINX)
# -----------------------------
resp = requests.post(
    f"{API_URL}/logout",
    params={"session_id": session_id}
)

if resp.status_code != 200:
    print("Logout failed")
    print("Status code:", resp.status_code)
    print("Response body:", resp.text)
    exit(1)

print(f"\nLogout successful for session_id={session_id}")

# -----------------------------
# Show DB state AFTER logout
# -----------------------------
print_db_state("DB1", DB_CONFIG_1)
print_db_state("DB2", DB_CONFIG_2)

print("\nCHECK COMPLETED SUCCESSFULLY")
