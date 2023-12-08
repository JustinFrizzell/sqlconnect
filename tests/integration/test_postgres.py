# Need sqlconnect.yaml
# Need sqlconnect.env

# Use a fixture to copy yaml and env
# test functions

import pytest
from pathlib import Path
import pandas as pd
import sqlconnect as sc


@pytest.fixture(scope="function")
def setup_env():
    source_env = Path("tests/integration/inputs/sqlconnect.env")
    target_env = Path("sqlconnect.env")

    # Setup: Copy the file to the target location
    target_env.write_text(source_env.read_text())

    # Yield control to the test
    yield

    # Cleanup: Remove the file after the test is done
    if target_env.exists():
        target_env.unlink()


@pytest.fixture(scope="function")
def setup_connections():
    source_env = Path("tests/integration/inputs/sqlconnect.yaml")
    target_env = Path("sqlconnect.yaml")

    # Setup: Copy the file to the target location
    target_env.write_text(source_env.read_text())

    # Yield control to the test
    yield

    # Cleanup: Remove the file after the test is done
    if target_env.exists():
        target_env.unlink()


def test_my_function(setup_env, setup_connections):
    conn = sc.Sqlconnector("Postgres_Test")

    migration = """
    CREATE TABLE public.employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        role VARCHAR(100)
    );
    INSERT INTO public.employees (name, role) VALUES 
    ('Alice Smith', 'Software Engineer'),
    ('Bob Johnson', 'Project Manager'),
    ('Carol Williams', 'Data Analyst');
    """
    conn.execute_sql_str(migration)

    df = conn.sql_to_df_str("SELECT * FROM public.employees")

    ids = [1, 2, 3]
    names = ["Alice Smith", "Bob Johnson", "Carol Williams"]
    roles = ["Software Engineer", "Project Manager", "Data Analyst"]

    # Create a DataFrame
    expected = pd.DataFrame({"id": ids, "name": names, "role": roles})

    pd.testing.assert_frame_equal(df, expected)
