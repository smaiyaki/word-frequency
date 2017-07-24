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

Python3 should be already installed on your machine.. you can test by running the command `python3` this should take you directly to the python3 interpreter with the version saying.. get to know where your python is installed by running the command `which python3' and keep note of the location. we will need it in the next step. In my case, it is `/usr/local/bin/python3`. If you dont have python3 installed follow the guide in this [guide](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04)

Now because we will want to isolaate our development environment from others, we need to create an environment with the help of the and point the environment to python3.. This is done with the following steps:
* `pip install virtualenv`
* Install the [virtaulenwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) using `pip install virtualenvwrapper`
* Then export WORKON_HOME=~/Envs
* mkdir -p $WORKON_HOME
* source /usr/local/bin/virtualenvwrapper.sh
* Finally we create our isolated environmnt using the command
 `mkvirtualenv octopos --python=/usr/local/bin/python3`

### Development of the APP ###
This is highly commented in the source code with best coding practice. I am basically scrapping the URL provided using the [beautifulSoup](https://pypi.python.org/pypi/beautifulsoup4), use the [natural language toolkit](http://www.nltk.org/data.html#command-line-installation) (NLTK) to process the words by removing punctuations and [stop words](https://en.wikipedia.org/wiki/Stop_words) (commonly used words like "i", "you"). In other to certify the requirement of asymmetrical encryption, we will install the [cryptography](http://python-guide-pt-br.readthedocs.io/en/latest/scenarios/crypto/) library. All the above libraries mentioned and many others required to run this app are in the file requirements.txt. Its contents looks like:
```
--find-links wheelhouse
wheel
alembic==0.9.3
asn1crypto==0.22.0
beautifulsoup4==4.4.1
cffi==1.10.0
click==6.7
cryptography==2.0
Flask==0.12.2
Flask-Migrate==1.8.0
Flask-Script==2.0.5
Flask-SQLAlchemy==2.1
idna==2.5
itsdangerous==0.24
Jinja2==2.9.6
Mako==1.0.7
MarkupSafe==1.0
mysqlclient==1.3.10
nltk==3.2
pycparser==2.18
python-dateutil==2.6.1
python-editor==1.0.3
requests==2.9.1
six==1.10.0
SQLAlchemy==1.1.11
Werkzeug==0.12.2
```
The first line is not required but its a hack I had to use to fix a bug with azure deployment. More on that in later section. To run this application, you issue the command:

* `pip install -r requirements.txt` to install the python modules in your environment
* `mkdir -p nltk_data` the directory that willm be used to download the tokenizer needed by NLTK
* `python -m nltk.downloader -d ./nltk_data/ all` download the tokenzers as explained in [here](http://www.nltk.org/data.html#command-line-installation)
* `python manage.py db init` to inintialise alembic (a lightweght database migration tool)
* `python manage.py db migrate` this creates the "migrations" folder with instructions on how to create the db
* `python manage.py db upgrade` to do the actual migration which involves creating the database struction from the defintion of the models in *models.py*
* `python manage.py runserver` this should start the app and reachable on port 5000.
* Try accessing http://localhost:5000/ and try with the url http://example.com .. it will work and deploy the result as per ![screenshot](https://github.com/smaiyaki/word-frequency/blob/master/Screen%20Shot%202017-07-24%20at%2000.45.33.png)

As you can see, this has achieved up to partial fullfilment of requirement 5 of the exercise. I couldn't make it to the last requirement due to challenges I faced with deployments.

### Deployments ###
I have tried deploying on Azure. I made considerable progress but missing out in the final stages. my app is accessible on http://wordcount.azurewebsites.net/. The firs issue I faced was the inability to install the critical python modules as described in this [page](https://github.com/Azure/azure-sdk-for-python/issues/1044). I had to manually download the modules wheel files as described in https://github.com/Azure/azure-sdk-for-python/issues/1044

I reached a stage where the app is says it has deployed successfully, but it appears to juts stop at doing the pip install only. It does not go beyond. I tried to solve that issue by adding a custom `deploy.cmd` file but that did not help me as well. see ![screesnhot](https://github.com/smaiyaki/word-frequency/blob/master/Screen%20Shot%202017-07-24%20at%2001.24.36.png)

I have now switch to using the AWS ebs for the deployment and the URL is available at http://octopos-test.eu-west-2.elasticbeanstalk.com/



