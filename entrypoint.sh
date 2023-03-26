#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
    python manage.py flush --no-input
    python manage.py migrate
    python3 manage.py loaddata marastoredata.json
fi



exec "$@"
