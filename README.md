Python web app for storing secrets in a SQLite database using a simple back-end build in FastAPI.
Template's front-end are build with Jinjia.

For running code follow this step:
- Download repo
- You have to have python installed in local machine and have poetry library
- Move on repo with a cmd line program and execute following commands:
    - poetry install
    - poetry shell
    - uvicorn src.storing_key.main:app --port 5000
