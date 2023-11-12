""" Handles validating and loading the connection configuration file """
from pathlib import Path
import yaml


def get_connection_config(connection_name: str) -> dict:
    """Using pathlib to read the YAML file."""
    config_text = Path("connections.yaml").read_text(encoding="utf-8")
    config = yaml.safe_load(config_text)
    return config["connections"][connection_name]


def get_db_url(connection_name: str) -> str:
    """Returns a connection string"""
    connection_config = get_connection_config(connection_name)
    sqlalchemy_driver = connection_config["sqlalchemy_driver"]
    odbc_driver = connection_config["odbc_driver"]
    server = connection_config["server"]
    database = connection_config["database"]
    options = "&".join([f"driver={odbc_driver}"] + connection_config["options"])

    connection_string = f"{sqlalchemy_driver}://@{server}/{database}?{options}"
    return connection_string
