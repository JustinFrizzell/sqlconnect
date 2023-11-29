# Usage and Configuration

## Configuration

To use SQLconnect, create a `connections.yaml` file in the root of your project (or in your home directory) with the following example structure:

```yaml
connections:
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

Also create a `.env` file in the root of your project (or in your home directory) with the following example structure:

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

# Set up a database connection, all configuration is handled with connections.yaml and .env
connection = sc.Sqlconnector("Database_PROD")

# Assign the results of a query to a pandas DataFrame
df = connection.sql_to_df("your_query.sql")

# Explore the dataframe with pandas
print(df.describe())
```