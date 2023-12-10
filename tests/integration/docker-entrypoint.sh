#!/bin/sh

echo "Waiting for Postgres to start"
./tests/integration/wait-for-it.sh postgres_db:5432 

echo "Migrating database"
python ./tests/integration/migration.py

echo "Starting pytest"
python -m pytest