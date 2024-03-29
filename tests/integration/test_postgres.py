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
    source_env = Path("tests/integration/inputs/postgres_sqlconnect.env")
    target_env = Path().home() / "sqlconnect.env"

    target_env.write_text(source_env.read_text(encoding="utf-8"))

    yield

    if target_env.exists():
        target_env.unlink()


@pytest.fixture(scope="function")
def setup_connections():
    """Fixture to set up sqlconnect.yaml"""
    source_env = Path("tests/integration/inputs/postgres_sqlconnect.yaml")
    target_env = Path().home() / "sqlconnect.yaml"

    target_env.write_text(source_env.read_text(encoding="utf-8"))

    yield

    if target_env.exists():
        target_env.unlink()


def test_sql_to_df_str_postgres(setup_env, setup_connections):
    conn = sc.Sqlconnector("Postgres")

    df = conn.sql_to_df_str(
        "SELECT name FROM public.employees WHERE position = 'Data Engineer'"
    )

    expected = pd.DataFrame({"name": ["Jane Doe"]})

    pd.testing.assert_frame_equal(df, expected)


def test_sql_to_df_postgres(setup_env, setup_connections):
    conn = sc.Sqlconnector("Postgres")

    df = conn.sql_to_df("tests/integration/sql/test_employees.sql")

    expected = pd.DataFrame({"name": ["Jane Doe"]})

    pd.testing.assert_frame_equal(df, expected)


def test_execute_sql_str_postgres(setup_env, setup_connections):
    conn = sc.Sqlconnector("Postgres")
    conn.execute_sql_str(
        """ INSERT INTO public.employees
            (id, "name", "position", database_url)
            VALUES
            (3, 'John S', 'Data Engineer', 'http://example.com/db/johns');
        """
    )


def test_execute_sql_postgres(setup_env, setup_connections):
    conn = sc.Sqlconnector("Postgres")
    conn.execute_sql("tests/integration/sql/test_insert_record.sql")


def test_df_to_sql_postgres(setup_env, setup_connections):
    conn = sc.Sqlconnector("Postgres")

    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    conn.df_to_sql(df, "table_name", if_exists="append", index=False)
