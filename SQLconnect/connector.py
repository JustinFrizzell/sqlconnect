import os
import pandas as pd
import sqlalchemy
import yaml


class SQLconnector:
    def __init__(self, connection_name):
        self.connection_name = connection_name
        self.engine = None
        self._create_engine()

    def _create_engine(self):
        """Create a SQLAlchemy engine using configuration from a YAML file."""

        connection_config = self._load_config()
        database_url = self._construct_db_url(connection_config)
        self.engine = sqlalchemy.create_engine(database_url)

    def _load_config(self):
        """Load database configuration from a YAML file."""

        with open("connections.yaml", "r") as file:
            config = yaml.safe_load(file)
        return config["connections"][self.connection_name]

    def _construct_db_url(self, connection_config):
        """Construct the database URL from the configuration."""

        sqlalchemy_driver = connection_config["sqlalchemy_driver"]
        odbc_driver = connection_config["odbc_driver"]
        server = connection_config["server"]
        database = connection_config["database"]
        options = "&".join([f"driver={odbc_driver}"] + connection_config["options"])

        connection_string = f"{sqlalchemy_driver}://@{server}/{database}?{options}"
        print(connection_string)
        return connection_string
        # return r"mssql+pyodbc://@DESKTOP-Q3UR0VP\SQLEXPRESS/WideWorldImporters?driver=SQL+Server&trusted_connection=yes"

    def sql_query(self, query_path):
        """Executes a SQL query from a file and returns a pandas DataFrame."""

        try:
            with open(query_path, "r") as file:
                query = file.read()
                return pd.read_sql_query(query, self.engine)
        except Exception as e:
            raise RuntimeError(f"Error executing query: {e}")
