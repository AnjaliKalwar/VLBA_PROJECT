# Exercise

Develop a Python 3 program

```sh
main.py
```

This program will be invoked by user 'root' using the
following procedure

```sh
cd feature142
python main.py > output.txt
```

and should fulfill the task described below (cp. 'Task').

(Git) stage, commit, and push your changes to feature
branch 'feature142'. Check, if the green check-mark appears in the
Gitea Web application at feature branch 'feature142'. If it appears,
submit a pull request via the Gitea Web application. If not, check your code.
It did not pass the tests.

  
#### Timetable - success points and due dates

Finish the exercise *before* the below given due date. If the exercise is
successfully finished and checked, you will be rewarded with the respective
amount of success points.

|Exercise    |points (obtainable)                   |due date (finish before)|
|:--------:  |:--------:                            |:--------:              |
|142|3|28.11.2025|


#### Hints

- The Python version that runs on the test server will be 3.10.4. So, Python 3
  features up to version 3.10.4 are available.
  - On Linux, `which python3` (or `which python`) and `python3 --version` may help
    to find out about Python versions that are already installed on your system.
- For Python 3.x cp.
  - https://docs.python.org/3/index.html
- For a Python tutorials cp. e.g.
  - https://docs.python.org/3/tutorial/index.html (recommended)
  - https://wiki.python.org/moin/BeginnersGuide
  - https://www.w3schools.com/python/default.asp (interactive)
  - ...
- Do not import non-standard Python packages.
- Read the docs!

#### Task

Open file

```sh
input.txt
```

as input file. You find it in the 'exercises' folder of feature branch
'feature142'. Open it from within your Python program, process the
input file as described further below, and print the output to `stdout`, so
that it can be re-direct to `output.txt`.



Delete all lines containing 'n', then sort the remaining lines by the number of words in the line.
Print only the contents without that of column 8 (column numbering starts with 1) as `[number of words]:[line without column 8]`. Use the "tab" character (`\t`) to separate the columns from each other.

