from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/label", response_class=HTMLResponse)
def get_upload(request: Request):
    tag = "flower"
    result = "Type a number"
    return templates.TemplateResponse('label.html', context={'request': request, 'result': result, 'tag': tag})


@router.post("/label", response_class=HTMLResponse)
def post_upload(request: Request, tag: str = Form(...)):

    return templates.TemplateResponse('label.html', context={'request': request, 'tag': tag})
