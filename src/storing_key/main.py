from os import path
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.storing_key import get_db
from src.storing_key.cmd import (
    create_new_secret,
    delete_secret_from_db,
    get_secret_from_db,
    list_secrets,
)
from src.storing_key.db import models
from src.storing_key.db.crud import create_user, get_all_user
from src.storing_key.db.database import engine
from src.storing_key.utils.authorization import (
    AddKeyForm,
    DeleteKeyForm,
    RegistrationForm,
    ShowKeyForm,
    UserPassword,
)

# Create the database tables
try:
    models.Base.metadata.create_all(bind=engine)
    error_message = ""
except Exception as e:
    error_message = e.args[0]
    print(error_message)

# Initialize FastAPI app
app = FastAPI()

# Get relative path
path_str = Path(path.dirname(path.realpath(__file__)))
# Mount static file as css
app.mount("/static", StaticFiles(directory=path_str.joinpath("static")), name="static")

# Set templates html path
templates = Jinja2Templates(directory=path_str.joinpath("templates"))


## GET route
# Home page
@app.get("/", response_class=HTMLResponse)
async def home_page_get(
    request: Request, type_response: str = "none", db: Session = Depends(get_db)
):
    return templates.TemplateResponse(
        "add_user.html", {"request": request, "type_response": type_response}
    )


# add secret
@app.get("/add_secret", response_class=HTMLResponse)
async def add_secret_get(
    request: Request, type_response: str = "none", db: Session = Depends(get_db)
):
    return templates.TemplateResponse(
        "add_secret.html", {"request": request, "type_response": type_response}
    )


# delete secret
@app.get("/delete_secret", response_class=HTMLResponse)
async def delete_secret_get(
    request: Request, type_response: str = "none", db: Session = Depends(get_db)
):
    return templates.TemplateResponse(
        "delete_secret.html", {"request": request, "type_response": type_response}
    )


# show keys
@app.get("/list_keys", response_class=HTMLResponse)
async def list_keys_get(
    request: Request, type_response: str = "none", db: Session = Depends(get_db)
):
    return templates.TemplateResponse(
        "list_keys.html",
        {"request": request, "type_response": type_response, "keys": []},
    )


# show key
@app.get("/show_key", response_class=HTMLResponse)
async def show_key_get(
    request: Request, type_response: str = "none", db: Session = Depends(get_db)
):
    return templates.TemplateResponse(
        "show_key.html",
        {"request": request, "type_response": type_response, "key_password": []},
    )


## POST route
# Home page
@app.post("/", response_class=HTMLResponse)
async def create_user_post(
    response: Response,
    registration_form: RegistrationForm = Depends(RegistrationForm.as_form),
    db: Session = Depends(get_db),
):
    username = registration_form.username
    if username in get_all_user(db):
        response = RedirectResponse(
            url="/?type_response=UsernameNonUnivoco", status_code=302
        )
        return response
    password = registration_form.password
    user_psw = UserPassword()
    user_info = {"username": username, "hashed_password": user_psw.get_hash(password)}
    create_user(db, user_info)
    print("#- Username {} created".format(username))
    response = RedirectResponse(
        url="/?type_response=AccountRegistrato", status_code=302
    )
    return response


# Add secret
@app.post("/add_secret", response_class=HTMLResponse)
async def add_secret_post(
    response: Response,
    add_key_form: AddKeyForm = Depends(AddKeyForm.as_form),
    db: Session = Depends(get_db),
):
    response_func = create_new_secret(
        username=add_key_form.username,
        password=add_key_form.password,
        key=add_key_form.key,
        secret=add_key_form.secret,
        passphrase=add_key_form.passphrase,
        db=db,
    )
    response = RedirectResponse(
        url="/add_secret?type_response={}".format(response_func), status_code=302
    )

    return response


# Delete secret
@app.post("/delete_secret", response_class=HTMLResponse)
async def delete_secret_post(
    response: Response,
    delete_key_form: DeleteKeyForm = Depends(DeleteKeyForm.as_form),
    db: Session = Depends(get_db),
):
    response_func = delete_secret_from_db(
        username=delete_key_form.username,
        password=delete_key_form.password,
        key=delete_key_form.key,
        db=db,
    )
    response = RedirectResponse(
        url="/delete_secret?type_response={}".format(response_func), status_code=302
    )

    return response


# List keys
@app.post("/list_keys", response_class=HTMLResponse)
async def list_keys_post(
    response: Response,
    request: Request,
    list_keys_form: RegistrationForm = Depends(RegistrationForm.as_form),
    db: Session = Depends(get_db),
):
    list_keys, response_func = list_secrets(
        username=list_keys_form.username, password=list_keys_form.password, db=db
    )

    return templates.TemplateResponse(
        "list_keys.html",
        {"request": request, "type_response": response_func, "keys": list_keys},
    )


# show key
@app.post("/show_key", response_class=HTMLResponse)
async def show_key_post(
    response: Response,
    request: Request,
    show_key_form: ShowKeyForm = Depends(ShowKeyForm.as_form),
    db: Session = Depends(get_db),
):
    key_pass, response_func = get_secret_from_db(
        username=show_key_form.username,
        password=show_key_form.password,
        key=show_key_form.key,
        passphrase=show_key_form.passphrase,
        db=db,
    )
    return templates.TemplateResponse(
        "show_key.html",
        {"request": request, "type_response": response_func, "key_password": key_pass},
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.storing_key.main:app", host="127.0.0.1", port=5000, log_level="info"
    )
