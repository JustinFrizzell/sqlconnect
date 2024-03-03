# Usage

```bash
pip install sqlconnect
```

## Setup

To use SQLconnect, create a `sqlconnect.yaml` file in the working directory of your project (or in your home directory) with the following example structure:

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

Also create a `sqlconnect.env` file in the working directory of your project (or in your home directory) with the following example structure:

```bash
# This file should be kept secure and not checked into version control (add to .gitignore)
# Production Database Credentials
MSSQL_USERNAME=prodUsername
MSSQL_PASSWORD=actualprodPassword
POSTGRES_USERNAME=postgresProdUsername
POSTGRES_PASSWORD=actualprodPassword
```

Replace the example values with your actual database connection details. The database credentials will be taken from the environment file at runtime.

### sqlconnect.yaml

You can store the details of multiple databases in a single `sqlconnect.yaml` file using this structure:

``` yaml
connections:
  Database1:
    ...
  Database2:
    ...
  Database3:
    ...
  Database4:
    ...    
```

Each database configuration requires the following parameters:

- `dialect`: SQLAlchemy [dialect](https://docs.sqlalchemy.org/en/20/dialects/) used to communicate with the DBAPI. For example, `postgresql` for Postgres, `mssql` for Microsoft SQL Server, `mysql` for MySQL and `oracle` for Oracle.
- `dbapi`: [PEP 249](https://peps.python.org/pep-0249/) specified Python Database API. For example, `psycopg2` for Postgres, `pyodbc` for Microsoft SQL Server, `pymysql` for MySQL and `oracledb` for Oracle. SQLconnect comes bundled with those DPAPIs, however other databases may require a specific DBAPI to be installed in your python environment.
- `host`: hostname or IP address of the database server where the database is hosted.

These database parameters are optional:

- `username`: Reference to the username in `sqlconnect.env`. For example, ${MSSQL_USERNAME} would be substituted by MSSQL_USERNAME from `sqlconnect.env` at runtime.
- `password`: Reference to the password in `sqlconnect.env`. For example, ${MSSQL_PASSWORD} would be substituted by MSSQL_PASSWORD from `sqlconnect.env` at runtime.
- `options`: [Query parameter](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.query) options to be passed to the SQLAlchemy connection string. For example, `driver: 'ODBC Driver 17 for SQL Server'` resolves to `?driver=ODBC+Driver+17+for+SQL+Server`

### sqlconnect.env

Multiple usernames and passwords can be stored in `sqlconnect.env`. This file should be handled sensitively and not checked into version control. The database credentials specified in `sqlconnect.yaml` will be taken from the environment file at runtime.

## Examples

### Query from a file directly

```python
import sqlconnect as sc

# Set up a database connection, all configuration is handled with sqlconnect.yaml and sqlconnect.env
connection = sc.Sqlconnector("Database_PROD")

# Assign the results of a query to a pandas DataFrame
df = connection.sql_to_df("your_query.sql")

# Explore the dataframe with pandas
print(df.describe())
```

### Query from a Python string

```python
import sqlconnect as sc

# Set up a database connection, all configuration is handled with sqlconnect.yaml and sqlconnect.env
connection = sc.Sqlconnector("WWI")

df = connection.sql_to_df_str("SELECT * FROM wideworldimporters.sales.invoices")

# Explore the dataframe with pandas
print(df.describe())
```

### Execute a SQL command from a file

```python
import sqlconnect as sc

# Set up a database connection, all configuration is handled with sqlconnect.yaml and sqlconnect.env
connection = sc.Sqlconnector("WWI")

connection.execute_sql("create_tables.sql")
```

### Execute a SQL command from a Python string

```python
import sqlconnect as sc

# Set up a database connection, all configuration is handled with sqlconnect.yaml and sqlconnect.env
connection = sc.Sqlconnector("WWI")

connection.execute_sql_str("DROP VIEW sales.orders")
```

### Create a SQL database table from a DataFrame

``` python
import sqlconnect as sc
import pandas as pd

connection = sc.Sqlconnector("WWI")

df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

connection.df_to_sql(
    df, name="table_name", schema="Sales", if_exists="append", index=False
)
```
