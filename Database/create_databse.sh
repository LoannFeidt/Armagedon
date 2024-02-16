#! /bin/bash
source .env
createdb -h $HOST -p $PORT -U $DB_USER $DATABASE
psql -h $HOST -p $PORT -U $DB_USER -d $DATABASE -a -f Database/script.sql
