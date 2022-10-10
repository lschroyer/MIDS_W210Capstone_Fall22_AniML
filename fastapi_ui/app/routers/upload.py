import logging

from fastapi import Request, UploadFile, File, APIRouter
from fastapi.templating import Jinja2Templates
import aiofiles
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    destination_file_path = "images_uploads/"+file.filename #output file path
    try:
        contents = file.file.read()
        with open(destination_file_path, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

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
