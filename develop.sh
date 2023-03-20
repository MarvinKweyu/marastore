#!/bin/bash

# WIP

#  this script creates a database with the user and credentials provided ,installs the requirements in a created virtual environment, runs the migrations and eventually runs the server

# stop in case anything fails
set -e

# setup maradomadstore database
DB_NAME=${1:-maradomadstore}
DB_USER=${2:-maradomadstore}
DB_USER_PASS=${3:-maradomadstore}
sudo su p <<EOF
createdb  $DB_NAME;
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_USER_PASS';"
psql -c "grant all privileges on database $DB_NAME to $DB_USER;"
echo "Postgres User '$DB_USER' and database '$DB_NAME' created."
EOF


# set up virtual environment and install requirements
python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver