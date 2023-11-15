""" Contains SQLconnector class"""
from pathlib import Path
import pandas as pd
import sqlalchemy
from sqlalchemy import text
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

        self.__database_url = config.get_db_url(config_dict)

        self.__engine = None
        self.__create_engine()

    def __create_engine(self):
        """Create a SQLAlchemy engine using configuration from a YAML file."""
        self.__engine = sqlalchemy.create_engine(self.__database_url)

    def sql_to_df(self, query_path: str) -> pd.DataFrame:
        """Executes a SQL query from a file and returns a pandas DataFrame."""
        try:
            query = Path(query_path).read_text(encoding="utf-8")
            return pd.read_sql_query(query, self.__engine)
        except Exception as e:
            raise RuntimeError(f"Error executing query: {e}")

    def sql_to_df_str(self, query: str) -> pd.DataFrame:
        """Executes a SQL query from a string and returns a pandas DataFrame."""
        try:
            return pd.read_sql_query(query, self.__engine)
        except Exception as e:
            raise RuntimeError(f"Error executing query: {e}")

    def execute_sql(self, sql_path: str) -> None:
        """Executes a SQL command from a file."""
        with self.__engine.connect() as connection:
            trans = connection.begin()
            try:
                command = Path(sql_path).read_text(encoding="utf-8")
                command = text(command)
                connection.execute(command)
                trans.commit()  # Explicitly commit the transaction
            except Exception as e:
                trans.rollback()  # Rollback in case of an error
                print(f"An error occurred: {e}")

    def execute_sql_str(self, command: str) -> None:
        """Executes a SQL command from a string."""
        with self.__engine.connect() as connection:
            trans = connection.begin()
            try:
                command = text(command.replace("\n", " "))
                connection.execute(command)
                trans.commit()  # Explicitly commit the transaction
            except Exception as e:
                trans.rollback()  # Rollback in case of an error
                print(f"An error occurred: {e}")
