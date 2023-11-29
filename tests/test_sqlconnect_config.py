import pytest
import yaml
from sqlconnect import config

# Testing config.get_connection_config()

# Mock data for testing get_connection_config where a config path is supplied
TEST_CONFIG_DICT = {
    "connections": {
        "Database_DEV": {
            "sqlalchemy_driver": "mssql+pyodbc",
            "odbc_driver": "SQL+Server",
            "server": "dev-server.database.com",
            "database": "DevDB",
            "options": ["Trusted_Connection=Yes"],
        },
        "Database_TEST": {
            "sqlalchemy_driver": "mssql+pyodbc",
            "odbc_driver": "SQL+Server",
            "server": "test-server.database.com",
            "database": "TestDB",
            "username": "${DB_TEST_USERNAME}",
            "password": "${DB_TEST_PASSWORD}",
            "options": ["Trusted_Connection=No"],
        },
    }
}


@pytest.fixture
def mock_config_file_yaml(tmp_path):
    # Create a temporary YAML config file for testing
    config_file = tmp_path / "sqlconnect.yaml"
    yaml_content = yaml.dump(TEST_CONFIG_DICT)
    config_file.write_text(yaml_content)

    return config_file


def test_get_connection_config_dev(mock_config_file_yaml):
    # Test retrieval of Database_DEV connection config
    connection_config = config.get_connection_config(
        "Database_DEV", str(mock_config_file_yaml)
    )
    assert connection_config == TEST_CONFIG_DICT["connections"]["Database_DEV"]


def test_get_connection_config_test_with_env_vars(mock_config_file_yaml, monkeypatch):
    # Mock environment variables for Database_TEST
    monkeypatch.setenv("DB_TEST_USERNAME", "test_user")
    monkeypatch.setenv("DB_TEST_PASSWORD", "test_password")
    connection_config = config.get_connection_config(
        "Database_TEST", str(mock_config_file_yaml)
    )
    assert connection_config["username"] == "${DB_TEST_USERNAME}"
    assert connection_config["password"] == "${DB_TEST_PASSWORD}"


def test_get_connection_config_file_not_found():
    # Test FileNotFoundError if config file does not exist
    with pytest.raises(FileNotFoundError, match="^Config file not found in"):
        config.get_connection_config("Database_DEV", "file_does_not_exist.yaml")


def test_get_connection_config_invalid_connection_name(mock_config_file_yaml):
    # Test exception for invalid connection name
    with pytest.raises(KeyError):
        config.get_connection_config("invalid_connection", str(mock_config_file_yaml))


# Mock data with missing connection details
MISSING_DETAILS_CONFIG_DICT = {
    "connections": {
        "Database_MISSING": {
            # Assume 'server' and 'database' are required but missing
            "sqlalchemy_driver": "mssql+pyodbc",
            "odbc_driver": "SQL+Server",
        }
    }
}


@pytest.fixture
def mock_config_missing_details(tmp_path):
    # Create a temporary YAML config file with missing details
    config_file = tmp_path / "missing_details.yaml"
    yaml_content = yaml.dump(MISSING_DETAILS_CONFIG_DICT)
    config_file.write_text(yaml_content)
    return config_file


def test_get_connection_config_missing_details(mock_config_missing_details):
    # Test behavior when required details are missing
    with pytest.raises(KeyError):  # Replace with the expected exception or behavior
        config.get_connection_config(
            "Database_MISSING", str(mock_config_missing_details)
        )


# Testing config.get_db_url()


# Fixture for a basic connection configuration
@pytest.fixture
def basic_config():
    return {
        "sqlalchemy_driver": "mssql+pyodbc",
        "odbc_driver": "ODBC Driver 17 for SQL Server",
        "server": "my_server",
        "database": "my_database",
    }


# Test for correct connection string generation
def test_get_db_url_correct_connection_string(basic_config):
    expected_string = (
        "mssql+pyodbc://my_server/my_database?driver=ODBC Driver 17 for SQL Server"
    )
    assert config.get_db_url(basic_config) == expected_string


# Test for missing configuration keys
def test_get_db_url_missing_configuration_keys(basic_config):
    del basic_config["server"]
    with pytest.raises(KeyError):
        config.get_db_url(basic_config)


# Test for environment variable authentication
def test_get_db_url_env_var_authentication(monkeypatch):
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASS", "test_pass")
    configuration = {
        "sqlalchemy_driver": "mssql+pyodbc",
        "odbc_driver": "ODBC Driver 17 for SQL Server",
        "server": "my_server",
        "database": "my_database",
        "username": "${DB_USER}",
        "password": "${DB_PASS}",
    }
    expected_string = "mssql+pyodbc://test_user:test_pass@my_server/my_database?driver=ODBC Driver 17 for SQL Server"
    assert config.get_db_url(configuration) == expected_string


# Test for missing environment variables
def test_get_db_url_missing_environment_variables(monkeypatch, basic_config):
    basic_config.update({"username": "${DB_USER}", "password": "${DB_PASS}"})
    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_PASS", raising=False)
    with pytest.raises(EnvironmentError):
        config.get_db_url(basic_config)


# Test for empty configuration dictionary
def test_get_db_url_empty_configuration():
    with pytest.raises(KeyError):
        config.get_db_url({})
