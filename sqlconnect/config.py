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
            required_keys = ["sqlalchemy_driver", "odbc_driver", "server", "database"]
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


def get_db_url(connection_config: dict) -> str:
    """
    Constructs and returns a database connection string from the given configuration dictionary.

    This function builds a database connection string suitable for SQLAlchemy, using
    details provided in a configuration dictionary. It handles the inclusion of
    authentication details securely by retrieving them from environment variables if
    necessary.

    Parameters
    ----------
    connection_config : dict
        A dictionary containing the database connection parameters. Expected keys include
        'sqlalchemy_driver', 'odbc_driver', 'server', 'database', and optionally 'username',
        'password', and 'options'. The 'username' and 'password' can be environment variable
        keys enclosed in curly braces (e.g., "${ENV_VAR}").

    Returns
    -------
    str
        The constructed database connection string.

    Raises
    ------
    EnvironmentError
        If 'username' and/or 'password' are specified as environment variables in the configuration
        and these variables are not found in either the current directory's 'sqlconnect.env' file or the
        user's home directory 'sqlconnect.env' file.

    Examples
    --------
    >>> connection_config = {
    ...     "sqlalchemy_driver": "mssql+pyodbc",
    ...     "odbc_driver": "ODBC Driver 17 for SQL Server",
    ...     "server": "my_server",
    ...     "database": "my_database",
    ...     "username": "${DB_USER}",
    ...     "password": "${DB_PASS}"
    ... }
    >>> get_db_url(connection_config)
    'mssql+pyodbc://username:password@my_server/my_database?driver=ODBC Driver 17 for SQL Server'

    Notes
    -----
    The function checks for 'sqlconnect.env' files in the current directory and the user's home directory
    for environment variables if 'username' and 'password' are provided as environment variable keys.
    It uses `os.getenv` to retrieve these environment variables.
    """

    sqlalchemy_driver = connection_config["sqlalchemy_driver"]
    odbc_driver = connection_config["odbc_driver"]
    server = connection_config["server"]
    database = connection_config["database"]
    options = "&".join([f"driver={odbc_driver}"] + connection_config.get("options", []))

    # Check for username and password
    auth_details = ""
    if "username" in connection_config and "password" in connection_config:
        if Path("sqlconnect.env").exists():
            load_dotenv(Path("sqlconnect.env"))
        else:
            home_env_path = Path.home() / "sqlconnect.env"
            if home_env_path.exists():
                load_dotenv(home_env_path)

        env_username_key = connection_config["username"].strip("${}")
        env_password_key = connection_config["password"].strip("${}")
        username = os.getenv(env_username_key)
        password = os.getenv(env_password_key)

        if username is None or password is None:
            raise EnvironmentError(
                f"Environment variables '{env_username_key}' and/or '{env_password_key}' not "
                f"found in {Path('sqlconnect.env').absolute()} or {Path.home() / 'sqlconnect.env'}"
            )

        auth_details = f"{username}:{password}@"

    # Construct the connection string
    connection_string = (
        f"{sqlalchemy_driver}://{auth_details}{server}/{database}?{options}"
    )
    return connection_string
