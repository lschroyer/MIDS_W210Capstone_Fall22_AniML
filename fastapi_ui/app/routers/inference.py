import logging

import boto3
import json

from botocore.exceptions import ClientError
import os
import pathlib

from fastapi.responses import HTMLResponse
from fastapi import Request, Form, APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates/")

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

@router.get("/inference")
def main(request: Request):
    # clear contents when initializing the page
    filename = "../data/classification_prediction/yolo_v5_prediction_inference.json"
    open(filename, 'w').close()

    return templates.TemplateResponse("inference.html", {"request": request})




@router.get("/inference_post/{name1}", response_class=HTMLResponse)
def api_async_save(request: Request, name1: str):
    name1 = name1.replace(" ", "")
    name1 = name1.replace("\\", "")
    name1_dict = json.loads(name1)[0]

    filename = "../data/classification_prediction/yolo_v5_prediction_inference.json"

    with open(filename, "r") as file:
        try:
            data = json.load(file)
            data.append(name1_dict)
        except:
            data = [name1_dict]

    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

    return templates.TemplateResponse('inference.html', 
            context={'request': request, 
                    })

