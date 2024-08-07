from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Header,
    Request,
    Response,
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler

import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")
components = Jinja2Templates(directory="templates/components")


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit-register", response_class=HTMLResponse)
async def submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    print(f"Received email: {email}, password: {password}")
    register_new_user = register_user(name=name, email=email, password=password)
    if register_new_user:
        print("User registered successfully.")
        return HTMLResponse(
            content="Registration successful. Check your email.", status_code=200
        )
    else:
        print("User registration failed.")
        return HTMLResponse(
            content="There is already a user with this email.", status_code=400
        )
