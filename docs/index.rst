.. image:: https://raw.githubusercontent.com/JustinFrizzell/sqlconnect/main/docs/_static/logo.png
   :alt: sqlconnect Logo
   :align: center

.. raw:: html

   <div style="text-align: center;">
      <a href="https://github.com/JustinFrizzell/sqlconnect/actions/workflows/ci.yaml">
         <img src="https://github.com/JustinFrizzell/sqlconnect/actions/workflows/ci.yaml/badge.svg" alt="CI-testing">
      </a>
      <a href="https://pypi.org/project/sqlconnect/">
         <img src="https://img.shields.io/pypi/v/sqlconnect" alt="PyPI">
      </a>
      <a href="https://sqlconnect.readthedocs.io/en/latest/?badge=latest">
         <img src="https://readthedocs.org/projects/sqlconnect/badge/?version=latest" alt="Documentation Status">
      </a>
      <a href="https://github.com/JustinFrizzell/sqlconnect/blob/main/LICENCE">
         <img src="https://img.shields.io/badge/License-MIT-purple.svg" alt="License: MIT">
      </a>
      <a href="https://github.com/astral-sh/ruff">
         <img src="https://img.shields.io/badge/Code_Style-ruff-black" alt="Code style: ruff">
      </a>
   </div>
   <div style="height: 20px;"></div> <!-- Spacer -->

**SQLconnect** is a Python package for data analysts that simplifies connecting to SQL databases like Postgres, Microsoft SQL Server and Oracle. DataFrames can be directly populated from .sql files, and database tables can be directly populated from DataFrames. A configuration file ``sqlconnect.yaml`` is used to store database connection details and an environment file ``sqlconnect.env`` is used for secure credential management. As a thin wrapper around SQLAlchemy and Pandas, SQLconnect provides convenient access to robust and flexible SQL operations.

Contents
========

.. toctree::
   :maxdepth: 3
   :includehidden:

.. toctree::
   :maxdepth: 3
   :includehidden:
   :caption: User Guide

   usage
   documentation

.. toctree::
   :maxdepth: 2
   :includehidden:
   :caption: Development

   contributing
   Change Log <https://github.com/JustinFrizzell/sqlconnect/releases>
   Release History <https://pypi.org/project/SQLconnect/#history>

.. toctree::
   :hidden:
   :caption: Project Links

   GitHub <https://github.com/JustinFrizzell/sqlconnect>
   PyPI <https://pypi.org/project/sqlconnect/>
   Licence <https://github.com/JustinFrizzell/sqlconnect/blob/main/LICENCE>
