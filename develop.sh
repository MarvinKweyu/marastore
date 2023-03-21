#!/bin/bash

# WIP
#  This script creates a database with the user and credentials provided ,installs the requirements in a created virtual environment, runs the migrations and eventually runs the server

# stop in case anything fails
set -e

# setup maranomadstore database
DB_NAME=${1:-maranomadstore}
DB_USER=${2:-maranomadstore}
DB_USER_PASS=${3:-maranomadstore}

# # Create the user with the specified username and password
# sudo psql -U postgres  -c "CREATE USER $DB_USER WITH PASSWORD '$DB_USER_PASS';"

# # Create the database with the specified name and owner
sudo psql -U $DB_USER createdb $DB_NAME


# set up virtual environment and install requirements
python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements/local.txt
python3 manage.py migrate
python3 manage.py runserver