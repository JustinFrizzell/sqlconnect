from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
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
                "database_url": database_url,
            }
            connection.execute(employees.insert(), data_to_insert)
            connection.commit()
            print(f"Data inserted successfully into {connection.engine} ")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")


DATABASE_URLS = [
    "postgresql+psycopg2://postgres:mysecretpassword@postgres_db:5432/postgres",
    "mssql+pyodbc://sa:MySecretPassw0rd!@mssql_db:1433/master?driver=ODBC+Driver+17+for+SQL+Server",
    "oracle+oracledb://system:MySecretPassw0rd!@oracle_db:1521/?service_name=XE",
]

for url in DATABASE_URLS:
    create_table_and_insert_data(url)
