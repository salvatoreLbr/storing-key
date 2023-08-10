# Storing Secrets 👮‍♂️
[![python](https://img.shields.io/badge/Python-^3.7-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://github.com/tiangolo/fastapi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview 🧿
This repo contains code about a web app for storing secrets in a SQLite database using a simple back-end build in [FastAPI](https://github.com/tiangolo/fastapi). Front-end is build in Jinjia. Database is managed with [SQLAlchemy](https://www.sqlalchemy.org/)
This web app permit you to store secrets and show every time using password and passphrase.
During the first run code creates a SQLite file in repository.

## Requirements ⚠
For installing all libraries need for running code it is possible using [poetry](https://python-poetry.org/). In the folder there are all needed files: pyproject.toml and poetry.lock.

## Installation ⚙️
For running code follow this step:
- If you haven't poetry installed:
```bash
pip install poetry
poetry config virtualenvs.in-project True
```
- If you have already poetry installed:
```bash
poetry install
poetry shell
uvicorn src.storing_key.main:app --port 5000
```
