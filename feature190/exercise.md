# VLBA Assignment – Login System Using Docker, FastAPI, MySQL and Nginx

## Overview
This exercise implements a containerized login system using FastAPI, MySQL, and Nginx.
The system demonstrates reverse proxying, service-to-service communication, and
application-level database synchronization.

## Architecture
The application consists of the following services:

Client → Nginx → FastAPI → DB1 & DB2

- **FastAPI**: Backend REST API
- **MySQL (DB1 & DB2)**: Persistent data storage
- **Nginx**: Reverse proxy and single entry point

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

This demonstrates redundancy using application-level synchronization.

### Nginx
Nginx listens on port 8080 and forwards all incoming HTTP requests to FastAPI.
Clients never directly access FastAPI.

## Endpoints
- `POST /create_login`
- `POST /login`
- `POST /logout`

## Variables 
{"username":"string","password":"string"}
{"username":"vlba_AnjaliKalwar_1","password":"anjali070700"}
{"username":"Ironman","password":"Arc_Reactor"}