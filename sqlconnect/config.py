"""
This module provides functionality for loading and validating SQL database connection configurations,
used primarily by the Sqlconnector class for establishing database connections.

The module includes functions to retrieve connection configurations from a YAML file and to construct a 
database connection URL. It supports dynamic configuration through file paths and dictionaries, and handles 
secure storage of sensitive details (e.g., usernames and passwords) through environment variables.

Functions:
    get_connection_config: Retrieves the configuration for a specified connection from a YAML file.
    get_db_url: Constructs and returns a database connection string from a given configuration dictionary.

Used By:
    - Sqlconnector: This class in a separate module utilises the functions provided here to manage database 
      connections and operations.

Dependencies:
    - os: Used for environment variable management.
    - pathlib: For file path manipulations.
    - yaml: Required for parsing YAML configuration files.
    - dotenv: Used for loading environment variables from 'sqlconnect.env' files.

Example Usage:
    # Used within Sqlconnector class
    config = get_connection_config('my_connection')
    db_url = get_db_url(config)

Notes:
    - Configuration files should define connection parameters like 'sqlalchemy_driver', 'odbc_driver', 
      'server', 'database', and optionally 'username', 'password'.
    - Usernames and passwords should be referenced as environment variables in the format '${ENV_VAR}'.
    - Attempts to load 'sqlconnect.env' files from the current directory or the user's home directory for environment 
      variables.
"""
import os
from pathlib import Path
import yaml
from dotenv import load_dotenv
from sqlalchemy import URL


def get_connection_config(connection_name: str, config_path: str = None) -> dict:
    """
    Retrieves the configuration for a specified connection from a YAML file.

    This function searches for a YAML configuration file either in a provided path
    or in default locations. It reads the file and extracts the configuration for
    the specified connection name.

    Parameters
    ----------
    connection_name : str
        The name of the connection for which the configuration is to be retrieved.
    config_path : str, optional
        The path to the configuration file. If not provided, the function searches
        in 'sqlconnect.yaml' or 'sqlconnect.yml' in the current directory, and
        then in the user's home directory.

    Returns
    -------
    dict
        A dictionary containing the configuration for the specified connection.

    Raises
    ------
    FileNotFoundError
        If the configuration file cannot be found in any of the default or provided paths.

    Examples
    --------
    >>> get_connection_config("my_connection")
    { ... }  # Returns the configuration dictionary for 'my_connection'.

    >>> get_connection_config("my_connection", "/path/to/custom/config.yaml")
    { ... }  # Returns the configuration dictionary from the specified custom path.

    Notes
    -----
    The function uses `pathlib.Path` for path manipulations and `yaml.safe_load`
    for reading the YAML file.
    """

    config_paths = (
        [Path(config_path)]
        if config_path
        else [
            Path("sqlconnect.yaml"),
            Path("sqlconnect.yml"),
            Path.home() / "sqlconnect.yaml",
            Path.home() / "sqlconnect.yml",
        ]
    )

    for path in config_paths:
        if path.exists():
            config_text = path.read_text(encoding="utf-8")
            config = yaml.safe_load(config_text)

            connection_config = config["connections"].get(connection_name)
            if not connection_config:
                raise KeyError(
                    f"Connection configuration for '{connection_name}' not found"
                )

            # Check if all required keys are present
            required_keys = ["dialect", "dbapi", "host"]
            missing_keys = [
                key for key in required_keys if key not in connection_config
            ]
            if missing_keys:
                raise KeyError(
                    f"Missing required configuration keys: {', '.join(missing_keys)} for connection '{connection_name}'"
                )

            return connection_config

    raise FileNotFoundError(
        f"Config file not found in {Path('sqlconnect.yaml').absolute()} "
        f"or {Path.home() / 'sqlconnect.yaml'}"
    )


def get_db_url(connection_config: dict) -> URL:
    """
    Constructs and returns a database connection URL from the given configuration dictionary.

    This function builds a database connection URL for SQLAlchemy, using
    details provided in a configuration dictionary. It handles the inclusion of
    authentication details securely by retrieving them from environment variables if
    necessary.

    Parameters
    ----------
    connection_config : dict
        A dictionary containing the database connection parameters. Expected keys include
        'dialect', 'dbapi', 'host' and optionally 'username', 'password', and 'options'.
        The 'username' and 'password' can be environment variable keys enclosed in
        curly braces (e.g., "${ENV_VAR}").

    Returns
    -------
    URL
        The constructed database connection URL.

    Raises
    ------
    EnvironmentError
        If 'username' and/or 'password' are specified as environment variables in the configuration
        and these variables are not found in either the current directory's 'sqlconnect.env' file or the
        user's home directory 'sqlconnect.env' file.
    """

    # Required
    dialect = connection_config["dialect"]
    dbapi = connection_config["dbapi"]
    host = connection_config["host"]

    # Optional
    database = connection_config.get("database")
    username, password = get_credentials(connection_config)
    query = connection_config.get("options")

    return URL.create(
        f"{dialect}+{dbapi}",
        host=host,
        database=database,
        username=username,
        password=password,
        query=query,
    )


def load_environment_file(file_paths: list[Path]):
    """Load environment variables from the first existing .env file in the provided list of file paths."""
    for file_path in file_paths:
        if file_path.exists():
            load_dotenv(file_path)
            return True
    return False


def get_credentials(connection_config: dict) -> tuple:
    """
    Retrieves credentials from environment variables based on the provided connection configuration.
    If 'username' or 'password' keys are not present in connection_config, returns None for them.

    Parameters
    ----------
    connection_config (dict): A dictionary possibly containing keys 'username' and 'password' with environment variable names.

    Returns
    -------
    tuple: A tuple containing the username and password, or None for each if not found.
    """
    load_environment_file([Path("sqlconnect.env"), Path.home() / "sqlconnect.env"])

    env_username_key = connection_config.get("username")
    env_password_key = connection_config.get("password")
    if env_username_key:
        env_username_key = env_username_key.strip("${}")
    if env_password_key:
        env_password_key = env_password_key.strip("${}")

    # Get username and password from environment variables, or default to None.
    username = os.getenv(env_username_key) if env_username_key else None
    password = os.getenv(env_password_key) if env_password_key else None

    if (env_username_key and not username) or (env_password_key and not password):
        raise EnvironmentError(
            f"Environment variables '{env_username_key}' and/or '{env_password_key}' not "
            f"found in {Path('sqlconnect.env').absolute()} or {Path.home() / 'sqlconnect.env'}"
        )

    return username, password
