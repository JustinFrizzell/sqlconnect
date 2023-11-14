import setuptools
from pathlib import Path

setuptools.setup(
    name="SQLconnect",
    version="0.0.2",
    author="Justin Frizzell",
    description=""" Package to simplify connections to SQL databases. """,
    long_description=Path("README.md").read_text(encoding="utf=8"),
    long_description_content_type="text/markdown",
    url="https://github.com/JustinFrizzell/SQLconnect",
    packages=setuptools.find_packages(),
    install_requires=["pandas", "sqlalchemy", "pyyaml", "pyodbc", "python-dotenv"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Database",
    ],
    keywords="SQL database connection configuration data",
)
