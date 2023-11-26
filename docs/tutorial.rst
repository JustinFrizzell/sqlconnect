
============
Tutorial
============

Getting started
----------------------------------------------------------------------------------------------------
Here's a quick example to get you started:

.. code-block:: python

    import SQLconnect as sc

    # Set up a database connection, all configuration is handled with connections.yaml and .env
    connection = sc.SQLconnector("Database_PROD")

    # Assign the results of a query to a pandas DataFrame
    df = connection.sql_to_df("query.sql")

    # Explore the dataframe with Pandas
    print(df.describe())


Configuration
------------------------ 

To use SQLconnect, create a ``connections.yaml`` file in the root of your project directory with the following example structure:

.. code-block:: yaml

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
