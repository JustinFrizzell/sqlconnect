#!/bin/sh

# This script is used to set up the environment for the integration tests
# 1. Wait for database services to be ready to accept connections
# 2. Migrate the databases to provide data for testing
# 3. Initiate pytest tests

echo "Waiting for Postgres to start"
/app/tests/integration/setup/wait-for-it.sh postgres_db:5432 

echo "Migrating database"
python /app/tests/integration/setup/migration.py

echo "Starting pytest"
python -m pytest
