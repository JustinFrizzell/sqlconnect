import setuptools
from pathlib import Path

setuptools.setup(
    name="sqlconnect",
    version="0.2.1",
    author="Justin Frizzell",
    description="Package to simplify connections to SQL databases.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/JustinFrizzell/sqlconnect",
    project_urls={
        "Documentation": "https://sqlconnect.readthedocs.io/en/latest/",
        "Source": "https://github.com/JustinFrizzell/sqlconnect",
    },
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=["pandas", "sqlalchemy", "pyyaml", "pyodbc", "python-dotenv"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Database",
    ],
    keywords="SQL database connection configuration",
)
