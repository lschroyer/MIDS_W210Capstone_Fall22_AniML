# from tkinter.tix import Form
from fastapi import FastAPI, Request, UploadFile, File, Form
from pydantic import BaseModel

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import *
from .routers import analytics, label, upload, filter, review, inference, training


from datetime import datetime
from typing import List

app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(filter.router)
app.include_router(review.router)
app.include_router(label.router)
# app.include_router(upload.router)
app.include_router(training.router)
app.include_router(inference.router)
app.include_router(analytics.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

class Data(BaseModel):
    user: str

@app.post("/page/contact/submit")
def sumbit_message(request: Request):
    data = request.form()
    print(data)
    return "successfully received your message!"


