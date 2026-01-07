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

@startuml
skinparam componentStyle rectangle
skinparam wrapWidth 200
skinparam maxMessageSize 200

title CI/CD Pipeline – Login/Logout System (Drone + Docker)

actor Developer

node "Drone CI Runner\n(Ubuntu)" {

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


Developer --> "Drone Pipeline" : git push / PR

"test-nginx-routing\n(step)" --> "NGINX\nnginx:stable"
"run checks\n(step)\n(check.py)" --> "NGINX\nnginx:stable"

"NGINX\nnginx:stable" --> "FastAPI App\n(solution.py)" : HTTP requests
"FastAPI App\n(solution.py)" --> "MySQL DB1\nmysql:8.0" : SQL writes
"FastAPI App\n(solution.py)" --> "MySQL DB2\nmysql:8.0" : SQL writes
@enduml




PLANT UML IMAGE REFERENCE:
https://www.plantuml.com/plantuml/dpng/bP9HQzim4CVVzIcEF3MC95xeeEHXj6lO5cXBbhHi3u6Xs4SYOfzSwPJ66uLzXtt3VPATadeDMMheWsqu__NJxwGxzwmTXo9NVcMer4uNaDgYj8J4Kwvo18SfQrhak1TvSBhyQZ9UGZz9zkg5tboZztg1K_C3jpyL6nRAvQXtEOInAJ4tXF3drs-uiWj3FNdRm32jF6C19qDd2U4D36swGjTMIgTi7GnnZRajqIb5DaDenLoamYGGePlHoTqy48Ts2tug1SzDrD5wwwV_49_z5AFd3edHfkD4oD12cE9Kjbk7KHS8qYMcArz7vBijTCjAuf9_ZA-TwHJTsgJYQecr23WlNI9hMP3LjdNsvjFevjkCjXe3ptgUOqm071XCS2qSQShPJJMZiNKCPybEz74V-55xlXYFPhGx7UYVTfFJeyWxaRIEdc3laaHmXw4Q1nTb6LktUM1ZANPzPE_hQlhb2eOVtiwegFnzFZZh9izRPrhQqrvoUPo3xzcy0T5_9I8-0letDT3flFz_40QmC0nby4lemNYYLDCGHCJn2rBD0z6uL1qjnmMDXotgdszln-3mFeYoLurXeHs_ZSY9rGTd65y3wRyCEKVAGf7_1G00


REFERENCE LINKS:
1.https://fastapi.tiangolo.com/tutorial/body/#request-body-path-query-parameters
2.https://www.w3schools.com/sql/sql_create_table.asp
3.https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/
4.Used chatbots for error solving