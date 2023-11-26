from SQLconnect import SQLconnector

CONFIG_DICT = {
    "sqlalchemy_driver": "mssql+pyodbc",
    "odbc_driver": "SQL+Server",
    "server": "dev-server.database.com",
    "database": "DevDB",
    "options": ["Trusted_Connection=Yes"],
}


def test_sqlconnector_connection_name_with_config_dict():
    # Test that SQLconnector object connection name is correctly initialised

    # Creating an instance of SQLconnector
    connector = SQLconnector("test_connection", config_dict=CONFIG_DICT)

    # Assertions to check if the instance is initialised as expected
    assert connector.connection_name == "test_connection"
