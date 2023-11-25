""" Handles validating and loading the connection configuration file """
import os
from pathlib import Path
import yaml
from dotenv import load_dotenv


def get_connection_config(connection_name: str, config_path: str = None) -> dict:
    """Using pathlib to read the YAML file."""

    # List of potential paths for the configuration file
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
            return config["connections"][connection_name]

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
