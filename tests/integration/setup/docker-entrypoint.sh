#!/bin/sh

# This script is used to set up the environment for the CI tests
# 1. Migrate the databases to provide data for testing
# 2. Initiate pytest tests
# 3. Check python code is formatted with Black

echo "Migrating database"
python ./tests/integration/setup/migration.py

echo "Starting pytest"
python -m pytest

echo "Checking formatted with Black"
black --check .