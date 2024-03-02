#!/bin/sh

# This script is used to set up the environment for the CI tests
# 1. Migrate the databases to provide data for testing
# 2. Initiate pytest tests
# 3. Check python code with Ruff

echo "Migrating database"
python ./tests/integration/setup/migration.py

echo "Starting pytest"
python -m pytest

echo "Ruff linting"
if ! ruff check .; then
  echo "Linting issues found."
  exit 1
fi

echo "ruff formatting"
if ! ruff format --check .; then
  echo "Formatting issues found."
  exit 1
fi