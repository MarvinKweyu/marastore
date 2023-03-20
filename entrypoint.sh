
#! /bin/sh

echo "starting project"
set -e

# ensure postgres is healthy before applying migrationss

if ["$DATABASE" = "postgres"]
then
    echo " waiting for postgres ..."

    while !nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"

fi


exec "$@"
