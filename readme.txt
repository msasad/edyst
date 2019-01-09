LeaderBoard API

Author: Asad Siddiqui (msasad8@gmail.com)


DEPENDENCIES:
The application has been developed and tested with following software:
    Python 3.7.1
    PostgreSQL 10

Rquired Python modules and their versions can be found in the included
requirements.txt file.


RUNNING:
Make sure that you have PostgreSQL server installed and correct connection
parameters supplied in config.json file.

Install the required python modules by running

    pip install -r requirements.txt

(Using a virtual environment is highly recommended.)

Set up the flask environment by setting the environment variables
    export FLASK_APP=app.py
    export FLASK_ENV=development    # optional


Initialize the DB by issuing
    flask initdb

Start the development server by issuing
    flask run
