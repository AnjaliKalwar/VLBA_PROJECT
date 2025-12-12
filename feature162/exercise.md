# Exercise

Develop an Ansible playbook

```sh
playbook
```

The playbook will be invoked by user 'root' using the
following procedure

```sh
cd feature162
ansible-playbook -i inventory playbook
```

The playbook should fulfill the task described below (cp. 'Task').

(Git) stage, commit, and push your changes (the playbook file) to feature
branch 'feature162'. Check, if the green check-mark appears in the
Gitea Web application at feature branch 'feature162'. If it appears,
submit a pull request via the Gitea Web application. If not, check your code.
It did not pass the tests.

  
#### Timetable - success points and due dates

Finish the exercise *before* the below given due date. If the exercise is
successfully finished and checked, you will be rewarded with the respective
amount of success points.

|Exercise    |points (obtainable)                   |due date (finish before)|
|:--------:  |:--------:                            |:--------:              |
|162|6|12.12.2025|


#### Hints

- The Ansible version will be the one that comes with Ubuntu 20.04.
- For Ansible and built-in modules cp.
  - https://www.ansible.com/
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html
- For information about Nginx's load balancer mode see
  - https://ubuntu.com/tutorials/install-and-configure-nginx
  - https://nginx.org/en/docs/beginners_guide.html
  - https://nginx.org/en/docs/ngx_core_module.html
  - https://nginx.org/en/docs/http/load_balancing.html
- Information about Apache2 are available at
  - https://httpd.apache.org/
- Information about Tomcat are available at
  - http://tomcat.apache.org/ -> Search in download archive for version stated in the task
  - https://linuxize.com/post/how-to-install-tomcat-9-on-ubuntu-20-04/
- In case of Nginx doesn't restart with `service nginx restart`, consider
  using alternative methods as `/etc/init.d/nginx restart`, or
  `nginx -g 'daemon off;'` instead.
- Read the docs!

#### Task

Write an Ansible playbook 'playbook'. It should set up Nginx as a
load balancer that routes requests to a Tomcat and an Apache 2 node
that act as Web servers.

The requests should be routed according to the following weights:

- Apache 2 node: 3
- Tomcat node: 1

And Nginx should use one worker process only.

The playbook will run on 'master.local'. All nodes are already
declared in an Ansible inventory file 'inventory', and public/private keys
are properly setup. The nodes run Ubuntu 20.04. 

Install Nginx on node 'node1.local'.

Install Apache 2 on node 'node2.local'. There, setup the `latest` version
of Apache 2 available. As we are using it as a Web server,
set up a valid HTML homepage for it that contains the string
'jyidngaysqja'.

Install Tomcat  on node 'node3.local'. There, setup version
'9.0.35' of Tomcat. Install it underneath `/usr/local`.
As we are using it as a Web server, set up a valid HTML homepage for it
that contains the string 'nruznijciesi'.