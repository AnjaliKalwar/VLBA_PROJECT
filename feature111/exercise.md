# Exercise

Clone your repository (its name is 'anjali.kalwar').
Locally (on your computer), switch to (feature) branch

```sh
'feature111'
```

by (Git) checking it out. Switch to folder 'feature111' and create a new file

```sh
myTestRepo.tar
```

by following the instructions given below (cp. 'Task').

After doing so, (Git) stage, commit, and push your changes. 
Check, if the green check mark appears in the Gitea Web application
at feature branch 'feature111'. If it appears, submit a *pull request* via 
the Gitea Web application. Do **not** close or merge the pull request yourself.
Just open it. According to the *feature branch workflow pattern*, the maintainer of the repo
(this is your lecturer) has to review and merge it.
Already closed or merged pull requests **will not be considered**.

  
#### Timetable - success points and due dates

Finish the exercise *before* the below given due date. If the exercise is
successfully finished and checked, you will be rewarded with the respective
amount of success points.

|Exercise    |points (obtainable)                   |due date (finish before)|
|:--------:  |:--------:                            |:--------:              |
|111|4|24.10.2025|


#### Hints

- Consider using `git clone`, `git switch`, `git add`, `git commit`,
`git push`, `tar` ...
- For `git` and `tar` see the respective `man` or `info` pages
- If you want to see a different branch in the Gitea Web application, you have
  to change it in the Web user interface

#### Task

Simulate the occurance and the fix of a Git merge conflict. Merge conflicts are 
common while working with version control systems. They often occur when merging two
branches, which	have the same file updated by two different	developers.

- In your local system, create a new folder. This folder **must not** be placed
  inside your Git repository that contains the checkout feature branch folder
  'feature111'. `cd` to the newly created folder. There, you shall simulate
  the merge conflict.
- Create a new Git repository. Name it 'myTestRepo'.
- In the following, act as user 'yfcgbo' with email
  'yfcgbo@email'.
- Take care that you repository's main branch is named 'main'.
- In 'main' branch create an empty file 'index.html'.
- Add the first line of code in that file as

  ```html
  <h1>this was added in main</h1>
  ```

  (Make sure that the file doesn't have any whitespace charaters or any extra
  lines.).

- Save the file and (Git) commit the changes. Use 'yfcgbo changed' as
  commit message. 
- Create a new branch 'vjly'.
- In the following, act as user 'pltnerlx' with email 'pltnerlx@email'.
- (Git) checkout to branch 'vjly'.

 and inside index.html file, paste the below line of code. Commit the changes.

- In the following, act as user 'pltnerlx' with email 
  'pltnerlx@email'.
- Add the following lines of code to file 'index.html' as

  ```html
  <h1>this was added in vjly</h1>
  <h1>this was added in vjly</h1>
  ```
- Save the file and (Git) commit the changes. Use 'pltnerlx changed' as
  commit message. 

- (Git) switch back to branch 'main'.
- In the following, again act as user 'yfcgbo' with email
  'yfcgbo@email'.
- Add the following lines of code to file 'index.html' as

  ```html
  <h1>this was added in main</h1>
  <h1>this was added in main</h1>
  ```
- Save the file and (Git) commit the changes. Use 'yfcgbo changed' as
  commit message. This will make branch 'main' one commit ahead of
  branch 'vjly' and also creates a conflict as both branches **can not**
  be merged automatically anymore.
- Now (Git) merge branch 'vjly' into branch 'main'. This
  will force the merge conflict to occur.
- Resolve the merge conflict by discarding the changes done by developer
  'pltnerlx' and commit the changes. Use 'yfcgbo merged and favors
  his solution' as commit message.
- Create a `tar` file of your repositry. Do not compress it, use 'cvf' as
  `tar` options, and name it 'myTestRepo.tar'.
- Finally, commit it as described at the top of the page.
