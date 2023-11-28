"""
The Sqlconnector class in this module is designed to aid database interactions using SQLAlchemy. 
It includes methods for establishing database connections, executing SQL queries and commands, 
and retrieving query results as pandas DataFrames. The class can be configured using either a 
configuration file or a dictionary.

Classes:
    Sqlconnector: A class to handle SQL database connections and operations.

Dependencies:
    - pandas: Used for handling query results as DataFrames.
    - sqlalchemy: Required for database connection and query execution.
    - pathlib: Utilised for handling file paths.
    - sqlconnect.config: A custom module for handling configuration details.

Example:
    >>> import sqlconnect as sc
    >>> 
    >>> # Set up a database connection. All configuration is handled with connections.yaml and .env
    >>> connection = sc.Sqlconnector("Database_PROD")
    >>> 
    >>> # Assign the results of a query to a pandas DataFrame
    >>> df = connection.sql_to_df("query.sql")
    >>> 
    >>> # Explore the dataframe with Pandas
    >>> print(df.describe())

Note:
    Configuration details for database connections should be provided either through
    a YAML file specified by `config_path` or a dictionary `config_dict`.
"""
from pathlib import Path
import pandas as pd
import sqlalchemy
from sqlalchemy import text
from sqlconnect import config


class Sqlconnector:
    """
    A class to handle SQL database connections and operations.

    This class provides methods to connect to a SQL database using SQLAlchemy,
    execute SQL queries, and perform database operations.

    Parameters
    ----------
    connection_name : str
        The name of the connection to be used. This name should correspond to an entry
        in the configuration file or dictionary.
    config_path : str, optional
        The file path of the configuration file. If not provided, a default configuration
        is used.
    config_dict : dict, optional
        A dictionary containing database connection configurations. If provided, it overrides
        the configurations from the file specified in `config_path`.

    Attributes
    ----------
    connection_name : str
        The name of the connection.
    engine : sqlalchemy.engine.Engine
        The SQLAlchemy engine object used for database connections.
    """

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

        self.engine = self.__create_engine()

    def __create_engine(self):
        """
        Create a SQLAlchemy engine using the database URL.

        Returns
        -------
        sqlalchemy.engine.Engine
            The created SQLAlchemy engine.

        Raises
        ------
        Exception
            If there is an error in creating the engine.
        """
        return sqlalchemy.create_engine(self.__database_url)

    def sql_to_df(self, query_path: str) -> pd.DataFrame:
        """
        Execute a SQL query from a file and return the results in a pandas DataFrame.

        Parameters
        ----------
        query_path : \
            The file path of the SQL query to be executed.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the results of the SQL query.

        Raises
        ------
        RuntimeError
            If there is an error in executing the query.
        """
        try:
            query = Path(query_path).read_text(encoding="utf-8")
            return pd.read_sql_query(query, self.engine)
        except Exception as e:
            raise RuntimeError(f"Error executing query: {e}")

    def sql_to_df_str(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query from a string and return the results in a pandas DataFrame.

        Parameters
        ----------
        query : str
            The SQL query to be executed.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the results of the SQL query.

        Raises
        ------
        RuntimeError
            If there is an error in executing the query.
        """
        try:
            return pd.read_sql_query(query, self.engine)
        except Exception as e:
            raise RuntimeError(f"Error executing query: {e}")

    def execute_sql(self, sql_path: str) -> None:
        """
        Execute a SQL command from a file.

        Parameters
        ----------
        sql_path : str
            The file path of the SQL command to be executed.

        Raises
        ------
        Exception
            If there is an error in executing the command.
        """
        with self.engine.connect() as connection:
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
        """
        Execute a SQL command from a string.

        Parameters
        ----------
        command : str
            The SQL command to be executed.

        Raises
        ------
        Exception
            If there is an error in executing the command.
        """
        with self.engine.connect() as connection:
            trans = connection.begin()
            try:
                command = text(command.replace("\n", " "))
                connection.execute(command)
                trans.commit()  # Explicitly commit the transaction
            except Exception as e:
                trans.rollback()  # Rollback in case of an error
                print(f"An error occurred: {e}")
