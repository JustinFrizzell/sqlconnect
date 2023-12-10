from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    text,
)
from sqlalchemy.exc import SQLAlchemyError

# Database credentials and connection details
DATABASE_URL = (
    "postgresql+psycopg2://postgres:mysecretpassword@postgres_db:5432/postgres"
)

# Create an engine instance
engine = create_engine(DATABASE_URL)

# Create a metadata instance
metadata = MetaData()

# Define the table
employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("database", String),
)

# Create the table in the database
metadata.create_all(engine)

try:
    with engine.connect() as connection:
        # Raw SQL query to insert data
        raw_sql = text(
            """
            INSERT INTO employees (id, name, position, database) 
            VALUES (:id, :name, :position, :database)
            """
        )

        # Example data to insert
        data_to_insert = {
            "id": 1,
            "name": "Jane Doe",
            "position": "Data Engineer",
            "database": "Postgres",
        }

        # Execute the query
        connection.execute(raw_sql, data_to_insert)

        # Commit the transaction
        connection.commit()

        print("Data inserted successfully.")

except SQLAlchemyError as e:
    print(f"An error occurred: {e}")
