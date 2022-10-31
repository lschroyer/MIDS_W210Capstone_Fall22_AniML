import logging
import boto3
from botocore.exceptions import ClientError
import os
import pathlib


from fastapi import Request, UploadFile, File, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
import aiofiles
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)
logging.info("end of logging configs")

@router.post("/upload")
def upload(file: UploadFile = File(...)):
    file_name = file.filename
    destination_file_path = "images_uploads/" + file_name #output file path
    logging.debug("Logging Test")
    try:
        contents = file.file.read()
        with open(destination_file_path, "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=404, detail="There was an error uploading the file")
    finally:
        file.file.close()

    try:
        s3 = boto3.client("s3")
        bucket_name = "famlive"
        bucket_folder = "training_upload"
        object_name = file_name 
        local_file_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "../../" + destination_file_path)

        response = s3.upload_file(local_file_path, bucket_name, '%s/%s' % (bucket_folder,object_name ))


    except Exception:
        raise HTTPException(status_code=400, detail="There was an error uploading the file to S3")
        

    return {"message": f"Successfuly uploaded {file.filename}"}


@router.get("/upload")
def main(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})
