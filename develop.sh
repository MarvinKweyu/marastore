#!/bin/bash

# WIP

#  this script creates a database with the user and credentials provided ,installs the requirements in a created virtual environment, runs the migrations and eventually runs the server

# stop in case anything fails
set -e

# setup maranomadstore database
DB_NAME=${1:-maranomadstore}
DB_USER=${2:-maranomadstore}
DB_USER_PASS=${3:-maranomadstore}
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