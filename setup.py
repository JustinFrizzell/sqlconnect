import setuptools
from pathlib import Path

setuptools.setup(
    name="sqlconnect",
    version="0.3.0",
    author="Justin Frizzell",
    description="Simplifies connections to SQL databases for data analysts. Populate DataFrames with the results of queries directly from .sql files.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/JustinFrizzell/sqlconnect",
    project_urls={
        "Documentation": "https://sqlconnect.readthedocs.io/en/latest/",
        "Source": "https://github.com/JustinFrizzell/sqlconnect",
    },
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=["pandas", "sqlalchemy", "pyyaml", "python-dotenv", "pyodbc", "psycopg2-binary", "oracledb", "PyMySQL"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Database",
    ],
    keywords="SQL database connection configuration",
)
