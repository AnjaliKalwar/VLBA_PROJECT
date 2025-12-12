# Exercise

Setup a working CI/CD pipeline by providing your own

```sh
.drone.yml
```

file for an application in this feature branch. Take the existing '.drone.yml' as
a basis and extend it. The commands therein will be invoked as soon 
as you push changes to this feature branch.

The application's task is described further below (cp. 'Task').

'.drone.yml' needs to be stored at your repo's root level. The other files should 
be stored in the folder 'feature190'. (Git) stage, commit, and push your changes.
Check, if the green check-mark appears in the
Gitea Web application at feature branch 'feature190'. If it does not appear,
check your code. It did not pass *your own* tests.

If you are done, issue a pull request.

  
#### Timetable - success points and due dates

Finish the exercise *before* the below given due date. If the exercise is
successfully finished and checked, you will be rewarded with the respective
amount of success points.

|Exercise    |points (obtainable)                   |due date (finish before)|
|:--------:  |:--------:                            |:--------:              |
|190|35|12.01.2026|


In addition, there will be an oral presentation, where you will have to live show case
your application with *other variable values* than those, that you used for the last
commit before your pull request.

Your presentation will be scheduled for one of the next three regular lecture sessions
*after* the task's due date given above.

It shall take around 10 to 15 minutes and encompass the following topics:

- use case and highlighted technology
- setup, architecture, and deployment (with PlantUML diagrams)
- live show case
- possible variations through changing variable settings

#### Hints

- Use `tmux` and `docker` for local tests before pushing
- For PlantUML and examples cp. https://plantuml.com/en/
- Read the docs!

#### Task


Create an own *IaaS/PaaS exercise* that 
- covers a new Linux technique that was not covered in the lecture, e.g. 
  - automate the setup of a distributed DBMS,
  - the setup of a development environment,
  - the setup of a session manager behind a reverse proxy,
  - or the setup of an identity server,
  - ...
- can vary according to variables with random values. 

Provide at least the following files:

- 'myexercise.var.md'  
  This Markdown file should describe the exercise, should contain variables as
 '{name_of_variable}', and should end with a section '# Variables', where each
variable is defined together with its possible values.
- 'myexercise.md'  
  This Markdown file should describe the exercise and should replace variables with
 a set of example values.
- 'mysolution'  
  This file should contain the main part of the exercise's solution. It should be a
 program, should define the variables to achieve variation at its beginning and may
 start other programs.
- 'mycheck'  
  This file should contain a test that runs after the exercise's solution run. It
 should be a program, should consider the defined variables to achieve variation, 
 and should check, if the file 'mysolution' setup and installed a correct 
 solution for the exercise and the respective example variable values.
- 'mydocs.md'  
  This Markdown file should describe your overall setup, the exercise, the rationale
 behind it, the solution, and the possible variations. It must at least contain a
 component diagram and a deployment diagram that is given in PlantUML source code. In 
 addition, it has to provide references and cite all parts taken from others, e.g. 
 from literature, from Web sites, from videos, from chat bots (cite as chat bot and 
 prompt), etc.

Your IaaS/PaaS exercise should

- use Ubuntu 24.04
- focus on a Linux technology that was *not* part of the lecture
- use at least one detached server as part of the CI/CD pipeline
- honor the fact that it needs to run in a resource-restricted environment

The final number of success points will be granted according to the degree of
fulfillment of the requirements given above.