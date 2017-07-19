# bucketlist
An API for a Bucket List service built using Flask.
The building blocks are:

* Python 3
* Flask

## Setting Up for Development

These are instructions for setting up bucketlist Flask app
in development environment.

* Clone the project code:

        $ git clone https://github.com/bmwachajr/bucketlist.git

* prepare virtual environment
  (with virtualenv you get pip, we'll use it soon to install requirements):

        $ cd bucketlist
        $ virtualenv --python=python3 bc-venv
        $ source bc-venv/bin/activate


* install requirements (Flask, ...) into virtualenv:

        $ pip install -r healthchecks/requirements.txt

* create database tables, triggers, superuser:

        $ ./db_create.py
        $ ./db_migrate.py 
        
* run development server:

        $ ./run.py

The site should now be running at `http://localhost:5080`
