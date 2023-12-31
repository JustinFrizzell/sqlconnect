import os
from pathlib import Path
import pytest
import pandas as pd
import sqlconnect as sc

if not os.environ.get("RUNNING_IN_DOCKER"):
    pytest.skip(
        "Skipping integration tests in local environment", allow_module_level=True
    )


@pytest.fixture(scope="function")
def setup_env():
    """Fixture to set up sqlconnect.env"""
    source_env = Path("tests/integration/inputs/oracle_sqlconnect.env")
    target_env = Path().home() / "sqlconnect.env"

    target_env.write_text(source_env.read_text(encoding="utf-8"))

    yield

    if target_env.exists():
        target_env.unlink()


@pytest.fixture(scope="function")
def setup_connections():
    """Fixture to set up sqlconnect.yaml"""
    source_env = Path("tests/integration/inputs/oracle_sqlconnect.yaml")
    target_env = Path().home() / "sqlconnect.yaml"

    target_env.write_text(source_env.read_text(encoding="utf-8"))

    yield

    if target_env.exists():
        target_env.unlink()


def test_sql_to_df_str_postgres(setup_env, setup_connections):
    conn = sc.Sqlconnector("Oracle")

    df = conn.sql_to_df_str(
        "SELECT name FROM SYSTEM.EMPLOYEES WHERE position = 'Data Engineer'"
    )

    expected = pd.DataFrame({"name": ["Jane Doe"]})

    pd.testing.assert_frame_equal(df, expected)
