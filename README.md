# Octopos Word Frequency test #

This file describes the steps to be used in replicating this test. It also document all the answers to the tasks prescribed.


### MySQL DB setup ###

There are two main methods of using MySQL in the google cloud; the  google cloud SQL which offers MySQL as a webservice and the manual deployment option on a google cloud compute VM. The main difference being that the former alleviates users from the stress of having to manage replications nd other database management tasks. Since this is a test with the code not for production use, I opted to go for the later (manual deployment). I followed the guide in this [document](https://cloud.google.com/solutions/setup-mysql) to set it up. Basically following the steps below:
* Setting up a Ubuntu VM on google cloud
* Updating packager with `sudo apt-get update`
* Installing MYSQL with the command `sudo apt-get -y install mysql-server`
* Running the command `sudo mysql_secure_installation` to set up a new password for the root
* In other to allow access from everywhere on the internet not only the google cloud internal network, I edited the file `/etc/mysql/mysql.conf.d/mysqld.cnf` and then set the **bind-address** to the internal ip of the server
`bind-address            = 10.128.0.2`
* Restart the service using the command: `sudo service mysql restart`
* Create our database using the command: `CREATE DATABASE octopos CHARACTER SET utf8 COLLATE utf8_bin;`
* Allow user called *generic* with password *generic* access to the DB.
`GRANT ALL PRIVILEGES ON octopos.* TO 'generic'@'%' IDENTIFIED BY 'generic';`
* Run a test to ensure that the database is indeed accessible by installing a mysql client on a local machine and connect
`sudo apt-get install mysql-client`
`mysql -h 130.211.185.22 -ugeneric -p` 
`show databases` will show you the *octopos* database.

### Set up Development environment ###
For this excersise, I am using the flask web framework for python. Also for convenience, python3 will be used for this excerise. We will therefore require on the bearest minimum, the following dependencies
1. Python3 installed
2. [Virtualenv](http://www.virtualenv.org/en/latest/)

Python3 should be already installed on your machine.. you can test by running the command `python3` this should take you directly to the python3 interpreter with the version saying.. get to know where your python is installed by running the command `which python3' and keep note of the location. we will need it in the next step. In my case, it is `/usr/local/bin/python3`


