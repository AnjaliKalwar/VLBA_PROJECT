# Exercise

Develop a Dockerfile

```sh
Dockerfile.main.df
```

A container will be build from it and invoked using the
following procedure

```sh
cd feature154
docker build -t feature154.main -f Dockerfile.main.df .
docker run --rm --name server.local feature154.main /bin/sh
docker exec server.local service nginx start
docker exec server.local service ssh start
```

So `ENTRYPOINT` or `CMD` directives are **not** needed.
The container should be developed according to the description below
(cp. 'Task').

(Git) stage, commit, and push your changes (the Docker file) to feature
branch 'feature154'. Check, if the green check-mark appears in the
Gitea Web application at feature branch 'feature154'. If it appears,
submit a pull request via the Gitea Web application. If not, check your code.
It did not pass the tests.

  
#### Timetable - success points and due dates

Finish the exercise *before* the below given due date. If the exercise is
successfully finished and checked, you will be rewarded with the respective
amount of success points.

|Exercise    |points (obtainable)                   |due date (finish before)|
|:--------:  |:--------:                            |:--------:              |
|154|5|21.11.2025|


#### Hints

- For Docker and 'Dockerfile' cp.
  - https://docs.docker.com/get-started/
  - https://docs.docker.com/engine/reference/builder/
- For Nginx installation and operation cp.
  - https://docs.nginx.com/nginx/
- For better understanding openSSH and ssh security in general cp.
  - https://www.openssh.com/
- Read the docs!

#### Task

Taking Ubuntu 22.04 as the base image, the container should install and setup
Nginx as a Web server. The Web server should deliver the Nginx default Web
page.

The running image will first be checked for

- using Nginx to serve Web pages,
- running on Ubuntu, and
- serving the Nginx default welcome page when called using

```sh
http://server.local
```

Furthermore, the container should install and setup an openSSH server, which
listens on port 22.

The openSSH server should be setup to allow for a passwordless, key-based
login for user 'root'. So, it is mandatory to pre-seed the server with the
public key of user 'root'.

Also change the settings of the SSH server to **deny**
password-based SSH login for all users.

The public key, that needs to be copied to the remote host and set up as the
user's 'root' public key, is stored as 'anjali.kalwar.public_key.pub' in the folder
'feature154'. The corresponding private key is also stored there
for testing purposes. The file is named 'anjali.kalwar.private_key.pem'.

Note that the provided public key was generated as part of an asymmetric, RSA
key pair. As such, it is correct. However, in order to work as a public key
as expected by open SSH, its
content must be provided with a starting 'ssh-rsa '. So, the resulting
public key **has to** look like this:

```txt
ssh-rsa<SPACE><generated public key as in 'anjali.kalwar.public_key.pub'>
```

The running image will further be checked for

- allowing key-based root login via `ssh`,
- denying password-based login via `ssh`, and
- the possibility to change the Nginx default welcome page via `ssh`.