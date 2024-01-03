import time
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.url import URL

MAX_RETRIES = 12

DATABASE_URLS = [
    URL.create(
        "postgresql+psycopg2",
        host="postgres_db",
        database="postgres",
        username="postgres",
        password="mysecretpassword",
    ),
    URL.create(
        "mssql+pyodbc",
        host="mssql_db",
        database="master",
        username="sa",
        password="MySecretPassw0rd!",
        query={"driver": "ODBC Driver 17 for SQL Server"},
    ),
    URL.create(
        "mysql+pymysql",
        host="mysql_db",
        database="sys",
        username="root",
        password="MySecretPassw0rd!",
    ),
    URL.create(
        "oracle+oracledb",
        host="oracle_db",
        username="system",
        password="MySecretPassw0rd!",
        query={"service_name": "XE"},
    ),
]


def create_employees_table(metadata):
    return Table(
        "employees",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(255)),
        Column("position", String(255)),
        Column("database_url", String(255)),
    )


def insert_data(engine, employees, data):
    try:
        with engine.connect() as connection:
            connection.execute(employees.insert(), data)
            connection.commit()
            print(f"Data inserted successfully into {connection.engine} ")
    except SQLAlchemyError as e:
        print(f"An error occurred during data insertion: {e}")


def create_table_and_insert_data(database_url):
    metadata = MetaData()
    employees = create_employees_table(metadata)

    for attempt in range(MAX_RETRIES):
        try:
            engine = create_engine(database_url)
            metadata.create_all(engine)
            data_to_insert = {
                "id": 1,
                "name": "Jane Doe",
                "position": "Data Engineer",
                "database_url": str(database_url),
            }
            insert_data(engine, employees, data_to_insert)
            break
        except SQLAlchemyError as e:
            if attempt < MAX_RETRIES - 1:
                print(
                    f"Connection attempt {attempt + 1} out of {MAX_RETRIES} failed to {engine.url.host}, retrying in 10 seconds..."
                )
                time.sleep(10)
            else:
                print(f"Max retries reached. Last error: {e}")


for url in DATABASE_URLS:
    create_table_and_insert_data(url)
