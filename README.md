rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses


1. Install VirtualBox if you dont have it in your system:
	https://www.virtualbox.org
2. Install Vagrant
	https://www.vagrantup.com
3. Navigate to vagrant/ directory of this repository in your local machine and run GitBash in 
	there. Alternatively, open GitBash anywhere and cd to the vagrant/ directory
4. Enter 'vagrant up'
	-this will initialize VirtualBox via Vagrant
5. Enter 'vagrant ssh'
	-this will log you in to the virtual machine that has been initialized
6. Enter cd /vagrant/tournament
	-Note that there is a '/' character before 'vagrant'
	-that means that folder is in the parent directory on where
	-vagrant is running
7. Run tournament_test.py by entering 'python tournament_test.py'