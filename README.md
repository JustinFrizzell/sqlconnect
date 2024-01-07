<div align="center">
  <img alt="SQLconnect logo" src="https://raw.githubusercontent.com/JustinFrizzell/sqlconnect/main/docs/_static/logo.png"><br>
</div>

---

<p align="center">
<a href="https://github.com/JustinFrizzell/sqlconnect/actions/workflows/ci.yaml"><img alt="CI-testing" src="https://github.com/JustinFrizzell/sqlconnect/actions/workflows/ci.yaml/badge.svg"></a>
<a href="https://pypi.org/project/sqlconnect/"><img alt="PyPI" src="https://img.shields.io/pypi/v/sqlconnect"></a>
<a href='https://sqlconnect.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/sqlconnect/badge/?version=latest' alt='Documentation Status' /></a>
<a href="https://github.com/JustinFrizzell/sqlconnect/blob/main/LICENCE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-purple.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

**SQLconnect** is a Python package designed to provide a straightforward way to interact with SQL databases (Postgres, Microsoft SQL Server, Oracle ect.). It enables direct population of DataFrames from .sql files. A `sqlconnect.yaml` file is used for database configuration and a `sqlconnect.env` file for secure credentials management.

## Features

- Turn SQL queries into DataFrames in as few as 3 lines of code

- Easy management of multiple database connections using a configuration file

- Secure storage of database credentials using environment variables

- Execute SQL queries and commands directly from .sql files or from a string

- Integration with SQLAlchemy & Pandas providing robust and flexible SQL operations

```python
import sqlconnect as sc

connection = sc.Sqlconnector("My_Database") # Set up a database connection based on sqlconnect.yaml

df = connection.sql_to_df("path/to/sql_query.sql") # Assign the results of a query to a DataFrame

print(df.describe()) # Explore the DataFrame with Pandas
```


## Configuration

To use SQLconnect, create a `sqlconnect.yaml` file in the root of your project (or in your home directory) with the following example structure:

```yaml
connections:
  My_Database:
    dialect: 'mssql'
    dbapi: 'pyodbc'
    host: 'prod-server.example.com'
    database: 'master'
    username: '${MSSQL_USERNAME}' # References MSSQL_USERNAME in sqlconnect.env
    password: '${MSSQL_PASSWORD}' # References MSSQL_PASSWORD in sqlconnect.env
    options: 
      driver: 'ODBC Driver 17 for SQL Server'

  A_Postgres_Database:
    dialect: 'postgresql'
    dbapi: 'psycopg2'
    host: 'dbserver123.company.com'
    database: 'postgres'
    username: '${POSTGRES_USERNAME}'
    password: '${POSTGRES_PASSWORD}'      
```

Also create a `sqlconnect.env` file in the root of your project (or in your home directory) with the following example structure:

```bash
# This file should be kept secure and not checked into version control (add to .gitignore)
# Production Database Credentials
MSSQL_USERNAME=prodUsername
MSSQL_PASSWORD=actualprodPassword
POSTGRES_USERNAME=postgresProdUsername
POSTGRES_PASSWORD=actualprodPassword
```

Replace the example values with your actual database connection details.

## Documentation

Full documentation for SQLconnect can be found at https://sqlconnect.readthedocs.io/

## Installation

```bash
pip install sqlconnect
```

## License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/JustinFrizzell/sqlconnect/main/LICENCE).
