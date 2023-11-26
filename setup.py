import setuptools
from pathlib import Path

setuptools.setup(
    name="SQLconnect",
    version="0.2.0",
    author="Justin Frizzell",
    description="Package to simplify connections to SQL databases.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/JustinFrizzell/SQLconnect",
    project_urls={
        "Documentation": "https://sqlconnect.readthedocs.io/en/latest/",
        "Source": "https://github.com/JustinFrizzell/SQLconnect",
        # You can add other links here if necessary
    },
    packages=setuptools.find_packages(),
    install_requires=["pandas", "sqlalchemy", "pyyaml", "pyodbc", "python-dotenv"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Database",
    ],
    keywords="SQL database connection configuration",
)
