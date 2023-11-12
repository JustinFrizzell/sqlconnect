import setuptools
from pathlib import Path

setuptools.setup(
    name="SQLconnect",
    version="0.0.1",
    description=""" Package to simplify connections to SQL databases. """,
    long_description=Path("README.md").read_text(encoding="utf=8"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["pandas", "sqlalchemy", "pyyaml", "pyodbc"],
)
