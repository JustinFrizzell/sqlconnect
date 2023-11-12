""" Contains SQLconnector class"""
from pathlib import Path
import pandas as pd
import sqlalchemy
from SQLconnect import config


class SQLconnector:
    """Class representing database connections"""

    def __init__(
        self, connection_name: str, config_path: str = None, config_dict: dict = None
    ):
        self.connection_name = connection_name

        if config_dict is None:
            if config_path is not None:
                # Instantiation with a config file path
                config_dict = config.get_connection_config(
                    connection_name, config_path=config_path
                )
            else:
                # Instantiation with only the connection name (default config)
                config_dict = config.get_connection_config(connection_name)

        self.database_url = config.get_db_url(config_dict)

        self.__engine = None
        self.__create_engine()

    def __create_engine(self):
        """Create a SQLAlchemy engine using configuration from a YAML file."""
        self.__engine = sqlalchemy.create_engine(self.database_url)

    def query_to_df(self, query_path: str) -> pd.DataFrame:
        """Executes a SQL query from a file and returns a pandas DataFrame."""
        try:
            query = Path(query_path).read_text(encoding="utf-8")
            return pd.read_sql_query(query, self.__engine)
        except Exception as e:
            raise RuntimeError(f"Error executing query: {e}")
