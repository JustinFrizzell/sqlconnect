from sqlconnect import Sqlconnector

CONFIG_DICT = {
    "sqlalchemy_driver": "mssql+pyodbc",
    "odbc_driver": "SQL+Server",
    "server": "dev-server.database.com",
    "database": "DevDB",
    "options": ["Trusted_Connection=Yes"],
}


def test_Sqlconnector_connection_name_with_config_dict():
    # Test that Sqlconnector object connection name is correctly initialised

    # Creating an instance of Sqlconnector
    connector = Sqlconnector("test_connection", config_dict=CONFIG_DICT)

    # Assertions to check if the instance is initialised as expected
    assert connector.connection_name == "test_connection"


# Test the sql functions for errors if given non-strings
