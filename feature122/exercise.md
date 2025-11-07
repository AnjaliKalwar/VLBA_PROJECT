# Exercise

Develop a (Ubuntu 22.04 bash) shell script

```sh
main.sh
```

This program will be invoked using the following procedure

```sh
cd feature122
chmod +x main.sh
bash ./main.sh < input.txt > output.txt
```

from user 'root'. Take file

```sh
input.txt
```

as input file. You find it in the 'exercises' folder of feature branch
'feature122'. Process the input file as described below (cp. 'Task'),
and copy your program that produces the output to

```sh
main.sh
```

Do not forget to (Git) stage, commit, and push your changes to feature
branch 'feature122'. Check, if the green check mark appears in the
Gitea Web application at feature branch 'feature122'. If it appears,
submit a pull request via the Gitea Web application. If not, check your code.
It did not pass the tests.

  
#### Timetable - success points and due dates

Finish the exercise *before* the below given due date. If the exercise is
successfully finished and checked, you will be rewarded with the respective
amount of success points.

|Exercise    |points (obtainable)                   |due date (finish before)|
|:--------:  |:--------:                            |:--------:              |
|122|4|07.11.2025|


#### Hints

- Useful commands may be, e.g. `sed`, `awk`, `grep`, `bc`, `cut`, `cat` ...
  - See the respective `man` or, often more detailed, `info` pages
  - If the commands (in case you are calling them in your bash script)
    are not pre-installed on the server, you will have to install them
    yourself as part of your bash script. Consider using `apt install` in
    unsupervised mode to do so.
  - Processing commands as user 'root' can also be tested locally, e.g. by
    using `sudo` (single command) or `sudo su` (multiple commands in a row,
    use `exit` to return to unprivileged user shell).
- For proper bash scripting and usage cp.
  - https://www.gnu.org/software/bash/manual/bash.html
- For proper use of regular expressions cp.
  - https://regex101.com/
- Read the docs!

#### Task


Delete all except every 2 st/nd/d/th line of column 7, output the resulting file.

