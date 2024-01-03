from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, URL
from sqlalchemy.exc import SQLAlchemyError


def create_table_and_insert_data(database_url):
    engine = create_engine(database_url)
    metadata = MetaData()

    employees = Table(
        "employees",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(255)),
        Column("position", String(255)),
        Column("database_url", String(255)),
    )

    metadata.create_all(engine)

    try:
        with engine.connect() as connection:
            data_to_insert = {
                "id": 1,
                "name": "Jane Doe",
                "position": "Data Engineer",
                "database_url": str(database_url),
            }
            connection.execute(employees.insert(), data_to_insert)
            connection.commit()
            print(f"Data inserted successfully into {connection.engine} ")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")


postgres_url = URL.create(
    "postgresql+psycopg2",
    host="postgres_db",
    database="postgres",
    username="postgres",
    password="mysecretpassword",
)

mssql_url = URL.create(
    "mssql+pyodbc",
    host="mssql_db",
    database="master",
    username="sa",
    password="MySecretPassw0rd!",
    query={"driver": "ODBC Driver 17 for SQL Server"},
)

oracle_url = URL.create(
    "oracle+oracledb",
    host="oracle_db",
    username="system",
    password="MySecretPassw0rd!",
    query={"service_name": "XE"},
)

mysql_url = URL.create(
    "mysql+pymysql",
    host="mysql_db",
    database="sys",
    username="root",
    password="MySecretPassw0rd!",
)


DATABASE_URLS = [
    postgres_url,
    mssql_url,
    oracle_url,
    mysql_url,
]

for url in DATABASE_URLS:
    create_table_and_insert_data(url)
