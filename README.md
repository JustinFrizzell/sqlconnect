<div align="center">
  <img alt="SQLconnect logo" src="https://raw.githubusercontent.com/JustinFrizzell/SQLconnect/main/images/logo.png"><br>
</div>

---

**SQLconnect** is a Python package designed to simplify the process of connecting to SQL databases. It uses a `connections.yaml` file to securely store database connection details and allows users to execute SQL queries stored in `.sql` files. This package is particularly useful for data analysts and developers who need a straightforward way to interact with SQL databases.

## Features

- Easy database connections using a YAML file.
- Execution of SQL queries directly from `.sql` files.
- Integration with pandas for seamless data manipulation.

## Installation

```bash
pip install SQLconnect
```

## Usage

Here's a quick example to get you started:

```python
import SQLconnect as sc

# Set up a database connection, all configuration is handled with connections.yaml and .env
connection = sc.SQLconnector("Database_PROD")

# Assign the results of a query to a pandas DataFrame
df = connection.sql_to_df("query.sql")

# Explore the dataframe with Pandas
print(df.describe())
```

## Configuration

To use SQLconnect, create a `connections.yaml` file in the root of your project directory with the following example structure:

```yaml
connections:
  Database_DEV:
    sqlalchemy_driver: 'mssql+pyodbc'
    odbc_driver: 'SQL+Server'
    server: 'dev-server.database.com'
    database: 'DevDB'   
    options:
      - 'Trusted_Connection=Yes'
      
  Database_TEST:
    sqlalchemy_driver: 'mssql+pyodbc'
    odbc_driver: 'SQL+Server'
    server: 'test-server.database.com'
    database: 'TestDB' 
    username: '${DB_TEST_USERNAME}' # References DB_TEST_USERNAME in .env
    password: '${DB_TEST_PASSWORD}' # References DB_TEST_PASSWORD in .env    
    options:
      - 'Trusted_Connection=No'

  Database_PROD:
    sqlalchemy_driver: 'mssql+pyodbc'
    odbc_driver: 'SQL+Server'
    server: 'prod-server.database.com'
    database: 'ProdDB'
    username: '${DB_PROD_USERNAME}' # References DB_PROD_USERNAME in .env
    password: '${DB_PROD_PASSWORD}' # References DB_PROD_PASSWORD in .env
    options:
      - 'Trusted_Connection=No'
```

Also create a `.env` file in the root of your project directory with the following example structure:

```bash
# This file should be kept secure and not checked into version control.
# Development Database Credentials
DB_TEST_USERNAME=devUser
DB_TEST_PASSWORD=devPassword

# Production Database Credentials
DB_PROD_USERNAME=prodUser
DB_PROD_PASSWORD=prodPassword
```

Replace the example values with your actual database connection details.

## License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/JustinFrizzell/SQLconnect/main/LICENCE).
