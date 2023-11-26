""" Handles validating and loading the connection configuration file """
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
        in 'connections.yaml' or 'connections.yml' in the current directory, and 
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
            Path("connections.yaml"),
            Path("connections.yml"),
            Path.home() / "connections.yaml",
            Path.home() / "connections.yml",
        ]
    )

    for path in config_paths:
        if path.exists():
            config_text = path.read_text(encoding="utf-8")
            config = yaml.safe_load(config_text)
            
            connection_config = config["connections"].get(connection_name)
            if not connection_config:
                raise KeyError(f"Connection configuration for '{connection_name}' not found")

            # Check if all required keys are present
            required_keys = ["sqlalchemy_driver", "odbc_driver", "server", "database"]
            missing_keys = [key for key in required_keys if key not in connection_config]
            if missing_keys:
                raise KeyError(f"Missing required configuration keys: {', '.join(missing_keys)} for connection '{connection_name}'")

            return connection_config

    raise FileNotFoundError(
        f"Config file not found in {Path('connections.yaml').absolute()} "
        f"or {Path.home() / 'connections.yaml'}"
    )


def get_db_url(connection_config: dict) -> str:
    """Returns a connection string from a dict"""

    sqlalchemy_driver = connection_config["sqlalchemy_driver"]
    odbc_driver = connection_config["odbc_driver"]
    server = connection_config["server"]
    database = connection_config["database"]
    options = "&".join([f"driver={odbc_driver}"] + connection_config.get("options", []))

    # Check for username and password
    auth_details = ""
    if "username" in connection_config and "password" in connection_config:
        if Path(".env").exists():
            load_dotenv(Path(".env"))
        else:
            home_env_path = Path.home() / ".env"
            if home_env_path.exists():
                load_dotenv(home_env_path)

        env_username_key = connection_config["username"].strip("${}")
        env_password_key = connection_config["password"].strip("${}")
        username = os.getenv(env_username_key)
        password = os.getenv(env_password_key)

        if username is None or password is None:
            raise EnvironmentError(
                f"Environment variables '{env_username_key}' and/or '{env_password_key}' not "
                f"found in {Path(".env").absolute()} or {Path.home() / ".env"}"
            )

        auth_details = f"{username}:{password}@"

    # Construct the connection string
    connection_string = (
        f"{sqlalchemy_driver}://{auth_details}{server}/{database}?{options}"
    )
    return connection_string
