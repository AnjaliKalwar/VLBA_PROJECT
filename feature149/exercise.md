# Exercise

Develop a Python 3 program

```sh
main.py
```

This program will be invoked by user 'root' using the
following procedure

```sh
cd feature149
python main.py
```

and should fulfill the task described below (cp. 'Task'). In case you
use non-standard Python modules it is also necessary to provide a file

```sh
requirements.txt
```

that lists these additionally needed Python modules. These modules will
be automatically installed through

```sh
pip install -r requirements.txt
```

(Git) stage, commit, and push your changes to feature
branch 'feature149'. Check, if the green check-mark appears in the
Gitea Web application at feature branch 'feature149'. If it appears,
submit a pull request via the Gitea Web application. If not, check your code.
It did not pass the tests.

  
#### Timetable - success points and due dates

Finish the exercise *before* the below given due date. If the exercise is
successfully finished and checked, you will be rewarded with the respective
amount of success points.

|Exercise    |points (obtainable)                   |due date (finish before)|
|:--------:  |:--------:                            |:--------:              |
|149|5|05.12.2025|


#### Hints

- The Python version that runs on the test server will be 3.10.4. 
- For better understanding ssh and ssh security in general cp. e.g.
  - https://www.openssh.com/
- Before connecting to it, it might be necessary to wait until the ssh server
  finished its starting procedure, and, in case the server needs a `restart`,
  consider using `reload` instead.
- The following **non-standard** Python modules may be helpful,
  e.g. `paramiko`, `fabric`, or `invoke`. For documentation cp. e.g.
  - https://www.paramiko.org/
  - http://www.fabfile.org/
  - https://www.pyinvoke.org/
- For a better understanding of `pip` refer to, e.g., `pip install --help`.
- Read the docs!

#### Task

Connect to the remote host 'server.local' via ssh by using login and password
to bootstrap using public/private keys for future connections.

The remote host listens on port 22, remote user is 'admin', and his password
is 'admin'.

The public key, that needs to be copied to the remote host and set up as the
user's 'admin' public key, is stored as 'public_key.pub' in the folder
'feature149'. The corresponding private key is also stored there
for testing purposes. The file is named 'private_key.pem'.

Note that the provided public key was generated as part of an asymmetric, RSA
key pair. As such, it is correct. However, in order to work as a public key
as expected by open SSH (the SSH server that runs on the remote host), its
content must be provided with a starting 'ssh-rsa '. So, the resulting
public key *has to* look like this:

```txt
ssh-rsa<SPACE><generated public key as in 'public_key.pub'>
```

After the public-key-based authentication was setup for user 'admin'

- change the sudo settings for user 'admin' to *allow for* passwordless `sudo`,

- also change the settings of the SSH server (openSSH is used here) to *deny*
  password-based SSH login for all users.