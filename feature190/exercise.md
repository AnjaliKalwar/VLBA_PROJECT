# VLBA Assignment – Login System Using Docker, FastAPI, MySQL and Nginx

## Overview
This exercise implements a containerized login–logout system using Docker,
FastAPI, MySQL, and NGINX, executed and validated through a CI/CD pipeline.

The system demonstrates:

- reverse proxying using NGINX

- service-to-service communication inside Docker

- application-level data consistency across multiple databases

- end-to-end validation in a resource-constrained CI environment

All components are executed as isolated containers and tested automatically.

## Architecture
The application consists of the following services:

Client → Nginx → FastAPI → DB1 & DB2

Components:

1. FastAPI (Ubuntu 24.04) – Backend REST API

2. Uvicorn – ASGI server running FastAPI on port 5000

3. MySQL DB1 & DB2 – Persistent storage (login_db)

4. NGINX – Reverse proxy and single entry point (port 80)

Clients and test scripts never access FastAPI directly.

## Services Description

### FastAPI
FastAPI provides REST endpoints for:
- User creation
- Login and session creation
- Logout

The application connects to both databases and writes data to both.

### MySQL
Two MySQL instances are used to store identical data:
- DB1
- DB2

Both databases store:
- users table
- sessions table
This demonstrates redundancy using application-level synchronization.

### Nginx
NGINX acts as the only externally accessible service.
- Listens on port 80
- Forwards requests to FastAPI (fastapi:5000)
- Exposes the /health endpoint for readiness checks

This ensures realistic production-like routing and isolation of backend services.

Clients never directly access FastAPI.

## Endpoints
- `POST /create_login`
- `POST /login`
- `POST /logout`
- `POST /health`

| Method | Endpoint        | Description                          |
| ------ | --------------- | ------------------------------------ |
| GET    | `/health`       | Readiness check                      |
| POST   | `/create_login` | Create a new user                    |
| POST   | `/login`        | Authenticate user and create session |
| POST   | `/logout`       | Remove session                       |


## Variables/Example Payloads:
- User creation and login

{"username":"string","password":"string"},
{"username":"vlba_AnjaliKalwar_1","password":"anjali070700"},
{"username":"Ironman","password":"Arc_Reactor"}

- logout

{"session_id":"Ironman_random_no"}