from fastapi import APIRouter, UploadFile, File, status, Depends
from sqlalchemy.orm import Session
from common.apiResponse import CommonResponse
from common.database import get_db
from . import image_controller

from common.apiResponse import CommonResponse

router = APIRouter(
    prefix="/images",
    tags=["이미지"]
)

UPLOAD_DIR = "uploaded_images"

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(file : UploadFile = File(...), db:Session = Depends(get_db)):
    new_image = image_controller.upload_image(db, file)
    
    result = {
        "imageId" : new_image.imageId,
        "url" : new_image.url
    }
    return CommonResponse.success_response(
        message="image_upload_success",
        result=result
    )
    