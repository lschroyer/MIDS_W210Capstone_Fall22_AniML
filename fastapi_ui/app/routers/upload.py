from fastapi import Request, UploadFile, File, APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open("uploaded_" + file.filename, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfuly uploaded {file.filename}"}

@router.get("/upload")
def main(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})
