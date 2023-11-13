# SQLconnect

SQLconnect is a Python package designed to simplify the process of connecting to SQL databases. It uses a `connections.yaml` file to securely store database connection details and allows users to execute SQL queries stored in `.sql` files. This package is particularly useful for data analysts and developers who need a straightforward way to interact with SQL databases.

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

# Establish a connection to the database
connection = sc.SQLconnector("WorldWideImporters")

# Assign the results of a query to a pandas DataFrame
df = connection.query_to_df("query.sql")

# Print the top 5 rows of the DataFrame
print(df.head(5))

# Print the connection details
print(f"connection_name: {connection.connection_name}")
print(f"database_url: {connection.database_url}")
```

## Configuration

To use SQLconnect, create a `connections.yaml` file in your project directory with the following example structure:

```yaml
connections:
  Database_DEV:
    sqlalchemy_driver: 'mssql+pyodbc'
    odbc_driver: 'SQL Server'
    server: 'dev-server.database.com'
    database: 'DevDB'
    options:
      - 'Trusted_Connection=Yes'
  Database_PROD:
    sqlalchemy_driver: 'mssql+pyodbc'
    odbc_driver: 'SQL Server'
    server: 'prod-server.database.com'
    database: 'ProdDB'
    options:
      - 'Trusted_Connection=Yes'
```

Replace the placeholder values with your actual database connection details.

## License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/JustinFrizzell/SQLconnect/main/LICENCE).