""" Contains SQLconnector class"""
from pathlib import Path
import pandas as pd
import sqlalchemy
from SQLconnect import config


class SQLconnector:
    """Class representing database connections"""

    def __init__(self, connection_name):
        self.connection_name = connection_name
        self.configuration = config.get_db_url(self.connection_name)
        self.__engine = None
        self.__create_engine()

    def __create_engine(self):
        """Create a SQLAlchemy engine using configuration from a YAML file."""
        self.__engine = sqlalchemy.create_engine(self.configuration)

    def query_to_df(self, query_path):
        """Executes a SQL query from a file and returns a pandas DataFrame."""
        try:
            query = Path(query_path).read_text(encoding="utf-8")
            return pd.read_sql_query(query, self.__engine)
        except Exception as e:
            raise RuntimeError(f"Error executing query: {e}")
