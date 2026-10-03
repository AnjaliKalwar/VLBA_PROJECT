# VLBA_PROJECT

This repository contains my project work for the **VLBA** course at **Otto von Guericke University Magdeburg (OVGU)**.

The repository is used to store and organize the different exercises and project implementations developed as part of the course.

## Repository

The complete project repository is available on GitHub:

**https://github.com/AnjaliKalwar/VLBA_PROJECT**

The repository contains the following exercises and projects:

VLBA_PROJECT/
├── feature111/
├── feature122/
├── feature142/
├── feature149/
├── feature152/
├── feature154/
├── feature162/
├── feature190/
├── .drone.yml
├── .gitignore
└── README.md

Each featureXXX directory represents an individual exercise or project developed during the course.


## Project Location

The current project implementation is located inside:

```text
VLBA_PROJECT/
    └── feature190/
```

The `feature190` directory contains the implementation of the **Login/Logout and Session Management** project.

## About the Project

The project implements a simple backend service for user login, logout, and session management.

The application provides functionality to:

* Create a user account
* Log in using user credentials
* Create and manage login sessions
* Log out and terminate a session
* Store user and session information in MySQL databases

The application is implemented as a containerized service and demonstrates the use of backend APIs, databases, reverse proxying, and container-based deployment.

## Technologies Used

The project uses the following technologies:

* **Python**
* **FastAPI** – backend REST API
* **MySQL** – database
* **Nginx** – reverse proxy
* **Docker** – containerization
* **Drone CI** – continuous integration and automated testing

## Application Architecture

The application consists of multiple services running in containers:

```text
                    Client
                      |
                      v
                   Nginx
                      |
                      v
                  FastAPI
                 /       \
                v         v
              DB1       DB2
            MySQL      MySQL
```

Nginx acts as the entry point for the application and forwards requests to the FastAPI backend.

The FastAPI application communicates with the MySQL databases to store and retrieve user and session information.

## Main API Operations

The application provides endpoints for the main authentication operations:

| Operation   | Endpoint        |
| ----------- | --------------- |
| Create user | `/create_login` |
| Login       | `/login`        |
| Logout      | `/logout`       |

## Project Files

The `feature190` directory contains the main files required to build, run, and test the application.

```text
feature190/
├── Dockerfile
├── nginx.conf
├── solution.py
├── check.py
├── exercise.md
├── exercise.var.md
└── .drone.yml
```

### Important Files

**`solution.py`**
Contains the FastAPI application and the implementation of the login, logout, and session functionality.

**`Dockerfile`**
Defines the container environment required to run the application.

**`nginx.conf`**
Contains the Nginx configuration used to forward incoming requests to the FastAPI service.

**`check.py`**
Contains checks used to verify the functionality of the implementation.

**`.drone.yml`**
Defines the Drone CI pipeline used for building and testing the project.

## Running the Project

The project is designed to run using containers.

After cloning the repository, navigate to the project directory:

```bash
cd VLBA_PROJECT/anjali.kalwar/feature190
```

The project can then be built and started using the provided Docker configuration.

## Purpose

This project demonstrates practical experience with:

* REST API development
* Backend development using Python and FastAPI
* Database integration
* Session management
* Docker-based application deployment
* Nginx reverse proxy configuration
* Automated testing and CI pipelines

## Author

**Anjali Kalwar**

M.Sc. Digital Engineering
Otto von Guericke University Magdeburg
