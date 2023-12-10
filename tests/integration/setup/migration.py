from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.exc import SQLAlchemyError

# Database credentials and connection details
DATABASE_URL = (
    "postgresql+psycopg2://postgres:mysecretpassword@postgres_db:5432/postgres"
)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the table
employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("database_url", String),
)

# Create the table in the database
metadata.create_all(engine)

try:
    with engine.connect() as connection:
        # Insert data
        data_to_insert = {
            "id": 1,
            "name": "Jane Doe",
            "position": "Data Engineer",
            "database_url": DATABASE_URL,
        }
        connection.execute(employees.insert(), data_to_insert)
        connection.commit()
        print("Data inserted successfully.")
except SQLAlchemyError as e:
    print(f"An error occurred: {e}")
