# VLBA Assignment – Variants and Design Decisions

## Use of Nginx
Nginx is used as a reverse proxy to provide a single entry point to the system.
All client requests are routed through Nginx before reaching the FastAPI service running at {fastapi_service_name}.

Example (from drone.yml):

Nginx service name: nginx

Nginx listens on port 80

## Nginx vs Uvicorn
Uvicorn is an ASGI server used to run the FastAPI application.
Nginx handles request routing and proxying but does not execute application code.

Nginx listens on {nginx_port}

FastAPI runs on {fastapi_port} using Uvicorn

Example (from drone.yml):

{nginx_port} = 80

{fastapi_port} = 5000

Uvicorn runs inside the fastapi service
## Database Design
Two MySQL databases are used to demonstrate redundancy.
Data is written to both databases by the application.

This approach ensures consistency without using native database replication.

Example (from drone.yml):

{db1_name} = login_db

{db2_name} = login_db

MySQL image: mysql:8.0.33

Credentials:

User: app_user

Password: app_password

## Docker Networking
All services communicate within the Docker network using service names.
No database ports are exposed to the host system.

Example:

FastAPI → DB1: host={db1_service_name}

FastAPI → DB2: host={db2_service_name}

Example (from drone.yml):

{db1_service_name} = db1

{db2_service_name} = db2

FastAPI environment variables:

DB1_HOST=db1

DB2_HOST=db2

Nginx accesses FastAPI via fastapi:5000
## Testing Approach
The {check_script_name} script validates the following:

Reverse proxy functionality via Nginx

API endpoint availability

Session creation and database state

End-to-end flow using one example user

For simplicity:

Passwords are stored in plain text

Session IDs are generated using random values

Example (from drone.yml):

{check_script_name} = check.py

API base URL: http://nginx

Health endpoint: /health

## Summary
The solution demonstrates container networking, reverse proxying,
and multi-database consistency using Docker and FastAPI.

## Future Scope
The current implementation focuses on demonstrating redundancy using dual databases
and a reverse proxy architecture.
Following points are furture scope enhancements
- Password hashing using secure algorithms such as bcrypt instead of plain-text storage.
- Token-based authentication (e.g., JWT)
- Automatic MySQL replication or synchronization mechanisms instead of application-level dual writes.
- Health checks and failover logic to dynamically switch database connections during failures. 

## Variables

{fastapi_service_name} – Name of the FastAPI Docker service (e.g., fastapi)

{fastapi_port} – Port used by FastAPI inside Docker (e.g., 5000)

{nginx_port} – Port exposed by Nginx (e.g., 80)

{db1_name} – Name of the first MySQL database (e.g., login_db)

{db2_name} – Name of the second MySQL database (e.g., login_db)

{db1_service_name} – Docker service name of the first MySQL database (e.g., db1)

{db2_service_name} – Docker service name of the second MySQL database (e.g., db2)

{check_script_name} – Script used to validate the system (e.g., check.py)