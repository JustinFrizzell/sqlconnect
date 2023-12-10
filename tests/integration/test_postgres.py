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

    df = conn.sql_to_df_str(
        "SELECT name FROM public.employees WHERE position = 'Data Engineer'"
    )

    expected = pd.DataFrame({"name": ["Jane Doe"]})

    pd.testing.assert_frame_equal(df, expected)
