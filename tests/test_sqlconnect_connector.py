from sqlconnect import Sqlconnector

CONFIG_DICT = {
    "dialect": "mssql",
    "dbapi": "pyodbc",
    "host": "dev-server.database.com",
    "database": "DevDB",
    "options": {"Trusted_Connection=": "Yes", "driver": "SQL Server"},
}


def test_Sqlconnector_connection_name_with_config_dict():
    # Test that Sqlconnector object connection name is correctly initialised

    # Creating an instance of Sqlconnector
    connector = Sqlconnector("Database_One", config_dict=CONFIG_DICT)

    # Assertions to check if the instance is initialised as expected
    assert connector.connection_name == "Database_One"
