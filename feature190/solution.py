#!/usr/bin/env python3
import os
import time
import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# -----------------------------
# DB Variables
# -----------------------------
DB1_HOST = os.environ.get("DB1_HOST", "localhost")
DB2_HOST = os.environ.get("DB2_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "app_user")
DB_PASS = os.environ.get("DB_PASS", "app_password")
DB_NAME = os.environ.get("DB_NAME", "login_db")

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

class UserRequest(BaseModel):
    username: str
    password: str

# -----------------------------
# DB connection helper
# -----------------------------
def get_conn(host):
    return mysql.connector.connect(
        host=host,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

# -----------------------------
# Initialize tables (robust)
# -----------------------------
def ensure_tables():
    for host in (DB1_HOST, DB2_HOST):
        for attempt in range(10):
            try:
                conn = get_conn(host)
                cur = conn.cursor()

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255)
                            COLLATE utf8mb4_bin
                            UNIQUE NOT NULL,
                        password VARCHAR(255)
                            COLLATE utf8mb4_bin
                            NOT NULL,
                        created_on DATETIME(6)
                            NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                    )
                """)

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id VARCHAR(255)
                            COLLATE utf8mb4_bin
                            PRIMARY KEY,
                        username VARCHAR(255)
                            COLLATE utf8mb4_bin
                            NOT NULL,
                        created_at DATETIME(6)
                            NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                    )
                """)

                conn.commit()
                cur.close()
                conn.close()
                break

            except mysql.connector.Error:
                time.sleep(1)

# -----------------------------
# Health check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# /create_login
# -----------------------------
@app.post("/create_login")
def create_login(data: UserRequest):
    ensure_tables()

    try:
        for host in (DB1_HOST, DB2_HOST):
            conn = get_conn(host)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users(username, password) VALUES (%s, %s)",
                (data.username, data.password)
            )
            conn.commit()
            cur.close()
            conn.close()

        return {"message": f"User '{data.username}' created on both DBs"}

    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")

# -----------------------------
# /login
# -----------------------------
@app.post("/login")
def login(data: UserRequest):
    conn = get_conn(DB1_HOST)
    cur = conn.cursor()
    cur.execute(
        "SELECT password FROM users WHERE BINARY username = %s",
        (data.username,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row or row[0] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = f"{data.username}_{os.urandom(4).hex()}"

    for host in (DB1_HOST, DB2_HOST):
        conn = get_conn(host)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sessions(session_id, username) VALUES (%s, %s)",
            (session_id, data.username)
        )
        conn.commit()
        cur.close()
        conn.close()

    return {"message": "Login successful", "session_id": session_id}

# -----------------------------
# /logout
# -----------------------------
@app.post("/logout")
def logout(session_id: str):
    for host in (DB1_HOST, DB2_HOST):
        conn = get_conn(host)
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM sessions WHERE BINARY session_id = %s",
            (session_id,)
        )
        conn.commit()
        cur.close()
        conn.close()

    return {"message": f"Session {session_id} logged out from both DBs"}

# -----------------------------
# Run FastAPI
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
