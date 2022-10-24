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
    destination_file_path = "images_uploads/"+file.filename #output file path
    file_name = file.filename
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
        # s3 = boto3.client('s3')
        # s3.meta.client.upload_file(destination_file_path, 's3://famlive/training_upload/', file.filename)
        # logging.info("------session attempt------")

        # s3 = boto3.resource('s3')
        # s3bucket = s3.Bucket('famlive').Object('training_upload')
        # # s3bucket = s3.Bucket('famlive').Object('training_upload/')
        # logging.info(s3bucket.name)

        # logging.info("-----bucket post attempt-----")
        # logging.info(destination_file_path)



        # client = boto3.client('s3')
        # # client.upload_file(destination_file_path, s3bucket.name)#, file.filename)
        # client.upload_file(Filename = destination_file_path, Bucket = "famlive", Key = file.filename)
        # # client.upload_file(destination_file_path, "^s3://famlive/training_upload/$", file.filename)

        s3 = boto3.client("s3")
        bucket_name = "famlive"
        bucket_folder = "training_upload"
        object_name = file_name #"sample_file.txt"
        # file_name = os.path.join(pathlib.Path(__file__).parent.resolve(), "sample_file.txt")
        local_file_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "../../" + destination_file_path)

        response = s3.upload_file(local_file_path, bucket_name, '%s/%s' % (bucket_folder,object_name ))


        # response = s3.upload_file(file_name, bucket_name, '%s/%s' % (bucket_folder, object_name))
        # # pprint(response)

        # logging.debug("-----S3 Debug-----")
        # s3 = boto3.client("s3")
        # bucket_name = "famlive"
        # bucket_folder = "training_upload"
        # object_name = "sample_file_Lucas.txt"
        # file_name = os.path.join(pathlib.Path(__file__).parent.resolve(), "sample_file_Lucas.txt")

        # response = s3.upload_file(file_name, bucket_name, '%s/%s' % (bucket_folder,object_name ))
    

        # s3 = boto3.client("s3")
        # bucket_name = "famlive"
        # bucket_folder = "training_upload"
        # object_name = "sample_file_Lucas_v2.txt"
        # file_name = os.path.join(pathlib.Path(__file__).parent.resolve(), "sample_file_Lucas_v2.txt")

        # response = s3.upload_file(file_name, bucket_name, '%s/%s' % (bucket_folder,object_name ))


    except Exception:
        raise HTTPException(status_code=400, detail="There was an error uploading the file to S3")
        # return {"message": "There was an error uploading the file to S3"}
        

    return {"message": f"Successfuly uploaded {file.filename}"}



# @router.post("/upload")
# async def upload(files: List[UploadFile] = File(...)):
#     for file in files:
#         destination_file_path = "images_uploads/"+file.filename #output file path
#         async with aiofiles.open(destination_file_path, 'wb') as out_file:
#             while content := await file.read(1024):  # async read file chunk
#               await out_file.write(content)  # async write file chunk
#     return {"Result": "OK", "filenames": [file.filename for file in files]}

# @router.post("/upload")
# def upload(files: List[UploadFile] = File(...)):
#     for file in files:
#         destination_file_path = "images_uploads/"+file.filename #output file path
#         try:
#             contents = file.file.read()
#             with open(destination_file_path, "wb") as f:
#                 f.write(contents)
#         except Exception:
#             return {"message": "There was an error uploading the file"}
#         finally:
#             file.file.close()
#     return {"message": "Successfuly uploaded"}
#

@router.get("/upload")
def main(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})
