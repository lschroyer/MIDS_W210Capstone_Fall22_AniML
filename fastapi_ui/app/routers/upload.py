from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/upload", response_class=HTMLResponse)
def get_upload(request: Request):
    tag = "flower"
    result = "Type a number"
    return templates.TemplateResponse('Upload.html', context={'request': request, 'result': result, 'tag': tag})


@router.post("/upload", response_class=HTMLResponse)
def post_upload(request: Request, tag: str = Form(...)):

    return templates.TemplateResponse('Upload.html', context={'request': request, 'tag': tag})
