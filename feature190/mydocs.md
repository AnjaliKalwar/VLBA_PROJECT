USER LOGIN-LOGOUT APPLICATION

This exercise implements a CI/CD-driven login-logout system using Docker-based services managed by Drone CI.
The system demonstrates how a modern web application can be tested automatically using detached infrastructure components, while remaining lightweight and suitable for a resource-restricted environment.

The solution combines:
    FastAPI (application logic)
    Uvicorn (ASGI server)
    NGINX (reverse proxy)
    Two MySQL databases (replicated backend state)
    Drone CI (pipeline orchestration)

All components are executed as isolated Docker containers.

The goal of this exercise is to design and validate a small web application that:
    exposes a REST API for user login/logout
    writes consistently to two independent databases
    is accessed exclusively through a reverse proxy
    is validated automatically via a CI/CD pipeline


This setup demonstrates several important infrastructure and platform concepts:
    Reverse proxy (NGINX)
    Application logic (FastAPI)
    Runtime server (Uvicorn)
    Persistent services (MySQL)

Databases and application services run independently of pipeline steps
Tests interact only through NGINX.

Solution Description:
1 - Application Logic

The FastAPI application exposes four endpoints:

GET /health : readiness and liveness check

POST /create_login : create a user on both databases

POST /login : authenticate and create a session

POST /logout : remove session from both databases


2 - CI/CD Pipeline

The Drone pipeline performs the following tasks:

Starts detached service containers:
    MySQL DB1
    MySQL DB2
    FastAPI (Ubuntu 24.04)
    NGINX reverse proxy
Steps:
Verifies routing and readiness using /health
Executes an end-to-end integration test (check.py)
Validates database consistency after each operation

All tests are performed without direct access to FastAPI, enforcing realistic reverse-proxy routing.


PLANT UML CODE:
@startuml
skinparam componentStyle rectangle
skinparam wrapWidth 200
skinparam maxMessageSize 200

title CI/CD Pipeline - Login/Logout System (Drone + Docker)

actor Developer

node "Drone CI Runner\n(Ubuntu Host)" {

  component "Drone Pipeline" {

   
    component "test-nginx-routing\n(step)"
    component "run checks\n(step)\n(check.py)"

  }

  node "Service Containers (Detached)" {

    node "NGINX\nnginx:stable" {
      component "Reverse Proxy\nPort 80"
    }

    node "FastAPI\nUbuntu 24.04" {
      component "Uvicorn\nPort 5000"
      component "FastAPI App\n(solution.py)"
    }

    node "MySQL DB1\nmysql:8.0" {
      database "login_db"
    }

    node "MySQL DB2\nmysql:8.0" {
      database "login_db"
    }
  }
}

Developer --> "Drone Pipeline" : git push / PR

"test-nginx-routing\n(step)" --> "NGINX\nnginx:stable"
"run checks\n(step)\n(check.py)" --> "NGINX\nnginx:stable"

"NGINX\nnginx:stable" --> "FastAPI App\n(solution.py)" : HTTP requests
"FastAPI App\n(solution.py)" --> "MySQL DB1\nmysql:8.0" : SQL writes
"FastAPI App\n(solution.py)" --> "MySQL DB2\nmysql:8.0" : SQL writes
@enduml


PLANT UML IMAGE REFERENCE:
https://www.plantuml.com/plantuml/dpng/bP9HQzim4CVVzIcEFZMC95xeeEHXj6lO6cXBbhHi3u6Xs4SYOfzKwPJ66uLzXtt3VPATqtZDijJG1zjm-kkdtrbt5bXxZaMkmjAGqruNaDh2MKBY2PSvWiUKDSrpt8ayUEs-c8mNq4kIdNgXrzSOWfxZn7p7pQ9YmqAv67Ol1Z0o3dD32Bz__e8hEpVKbRUD39CoC1PmFF1Mbj_0mAPBz2sbTChMmm1Nc5k7NYco6SBH9YTK64SYz5Cwlfj5uWYNDd3h27ue1S-TrFdw_EqwoFDFYZ5mcqHhtVPYPMWkO15phQFzg8y4wGBJPQWZyjqKEgwKkEGVgzUJxWJzogGYR8cr2FWWhI9hsP3LjdNsvjFmvkkKDXhzm7gMRtm1zWp6k1AEDENjkfpIo7g6q-H9z74N-547FXyDfxJzHRsJJd9o47adajRJ5lOkIGIt7wfnSEvSrRhD8njBLTS7phuk9v-lOF3XxPIACjpd_TDEydnqfgKz7IINLyFmBPir87glH5IFWFwE3hJRx_yVX3xC3OEBOG5T68sLQXg22d7uWbJpG3HkLGVBrOR6dotgbxUt8_1u7qKvgCQmq5wwZJvKrGTl65y3wRqCEKFAOf7_0G00