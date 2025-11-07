# Exercise

Develop a Dockerfile

```Docker
Dockerfile.main.df
```

A container will be build from it and invoked using the
following procedure

```sh
cd feature152
docker build -t feature152.main -f Dockerfile.main.df .
docker run --rm --name server.local \
       feature152.main /bin/sh
docker exec server.local <a commmand to start the web server>
```

So **no** docker `ENTRYPOINT` or `CMD` directives are needed.
The container should be developed according to the description below
(cp. 'Task').

(Git) stage, commit, and push your changes (the Docker file) to feature
branch 'feature152'. Check, if the green check-mark appears in the
Gitea Web application at feature branch 'feature152'. If it appears,
submit a pull request via the Gitea Web application. If not, check your code.
It did not pass the tests.

  
#### Timetable - success points and due dates

Finish the exercise *before* the below given due date. If the exercise is
successfully finished and checked, you will be rewarded with the respective
amount of success points.

|Exercise    |points (obtainable)                   |due date (finish before)|
|:--------:  |:--------:                            |:--------:              |
|152|3|14.11.2025|


#### Hints

- For Docker and Dockerfile cp.
  - https://docs.docker.com/get-started/
  - https://docs.docker.com/engine/reference/builder/
- Read the docs!

#### Task


Taking Ubuntu 22.04 as the base image, the container should install
and setup Caddy as a Web server. The Web server should deliver its
default Web page.


The running image will be checked for

- using the correct Web server to serve Web pages,
- running on Ubuntu, and
- serving the Web server's default welcome page when called under

```sh
http://server.local
```