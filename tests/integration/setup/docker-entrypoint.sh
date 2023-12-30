#!/bin/sh

# This script is used to set up the environment for the CI tests
# 1. Wait for database services to be ready to accept connections
# 2. Migrate the databases to provide data for testing
# 3. Initiate pytest tests
# 4. Check python code is formatted with Black

echo "Waiting for Postgres to start"
./tests/integration/setup/wait-for-it.sh postgres_db:5432 

echo "Waiting for MS SQL Server to start"
./tests/integration/setup/wait-for-it.sh mssql_db:1433 

echo "Migrating database"
python ./tests/integration/setup/migration.py

echo "Starting pytest"
python -m pytest

echo "Checking formatted with Black"
black --check .