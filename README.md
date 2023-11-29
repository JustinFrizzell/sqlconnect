<div align="center">
  <img alt="SQLconnect logo" src="https://raw.githubusercontent.com/JustinFrizzell/sqlconnect/main/docs/_static/logo.png"><br>
</div>

---

<p align="center">
<a href="https://pypi.org/project/sqlconnect/"><img alt="PyPI" src="https://img.shields.io/pypi/v/sqlconnect"></a>
<a href='https://sqlconnect.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/sqlconnect/badge/?version=latest' alt='Documentation Status' /></a>
<a href="https://github.com/JustinFrizzell/sqlconnect/blob/main/LICENCE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-purple.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

**SQLconnect** is a Python package designed to simplify the process of connecting to SQL databases. It uses a `sqlconnect.yaml` file for database configuration and a `sqlconnect.env` file for secure credentials management. SQLconnect supports executing SQL from `.sql` files or Python strings, and retrieving data into pandas DataFrames. This package is particularly useful for data analysts and developers who need a straightforward way to interact with SQL databases.

## Features

- Allows easy configuration and management of database connections using a `sqlconnect.yaml` file.

- Supports the use of a `sqlconnect.env` file for secure storage of database credentials, enhancing security.

- Leverages SQLAlchemy for database connections, providing a robust and flexible framework for SQL operations.

- Enables executing SQL queries and directly retrieving the results into pandas DataFrames, facilitating easy data manipulation and analysis.

- Capable of handling multiple database connections, allowing users to switch between different databases as needed.

- Provides functionality to execute SQL queries either by reading from an external file or directly from a string.

## Installation

```bash
pip install sqlconnect
```

## Configuration

To use SQLconnect, create a `sqlconnect.yaml` file in the root of your project (or in your home directory) with the following example structure:

```yaml
connections:
  Database_PROD:
    sqlalchemy_driver: 'mssql+pyodbc'
    odbc_driver: 'SQL+Server'
    server: 'prod-server.database.com'
    database: 'ProdDB'
    username: '${DB_PROD_USERNAME}' # References DB_PROD_USERNAME in sqlconnect.env
    password: '${DB_PROD_PASSWORD}' # References DB_PROD_PASSWORD in sqlconnect.env
    options:
      - 'Trusted_Connection=No'
```

Also create a `sqlconnect.env` file in the root of your project (or in your home directory) with the following example structure:

```bash
# This file should be kept secure and not checked into version control (add to .gitignore)
# Production Database Credentials
DB_PROD_USERNAME=prodUser
DB_PROD_PASSWORD=prodPassword
```

Replace the example values with your actual database connection details.

## Usage

Here's a quick example to get you started:

```python
import sqlconnect as sc

# Set up a database connection, all configuration is handled with sqlconnect.yaml and sqlconnect.env
connection = sc.Sqlconnector("Database_PROD")

# Assign the results of a query to a pandas DataFrame
df = connection.sql_to_df("your_query.sql")

# Explore the dataframe with pandas
print(df.describe())
```

## Documentation

Full documentation for SQLconnect can be found at https://sqlconnect.readthedocs.io/

## License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/JustinFrizzell/sqlconnect/main/LICENCE).
