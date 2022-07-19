from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from os import path
from pathlib import Path
from sqlalchemy.orm import Session

import uvicorn

from src.storing_key import get_db
from src.storing_key.db import models
from src.storing_key.db.database import engine

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
    request: Request, db: Session = Depends(get_db)
):
    return templates.TemplateResponse(
        "home_page.html", {"request": request}
    )

if __name__ == "__main__":
    uvicorn.run(
        "src.storing_key.main:app", host="127.0.0.1", port=5000, log_level="info"
    )
