# VLBA Assignment – Variants and Design Decisions

## Use of Nginx
Nginx is used as a reverse proxy to provide a single entry point to the system.
All client requests are routed through Nginx before reaching FastAPI.

## Nginx vs Uvicorn
Uvicorn is an ASGI server used to run FastAPI.
Nginx handles request routing and proxying but does not run application code.

## Database Design
Two MySQL databases are used to demonstrate redundancy.
Data is written to both databases by the application.

This approach ensures consistency without using native database replication.

## Docker Networking
Inside Docker, services communicate using service names.
Outside Docker, exposed ports and localhost are used.
Example:
- FastAPI → DB1: `host=db1`
- check.py → DB1: `host=localhost, port=3307`

## Testing Approach
The check script validates:
- Reverse proxy via NGINX
- API functionality
- Session creation (Database state)
- One user example end to end

Passwords are stored in plain text for simplicity.
Session IDs are generated using random values

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
