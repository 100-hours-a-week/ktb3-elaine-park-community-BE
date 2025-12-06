from fastapi import APIRouter, UploadFile, File, status
from typing import List, Dict, Any
import shutil
import uuid
import os
from common.database import IMAGE_DB, NEXT_IMAGE_ID
from . import image_controller

from common.apiResponse import CommonResponse

router = APIRouter(
    prefix="/images",
    tags=["이미지"]
)

UPLOAD_DIR = "uploaded_images"

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(file : UploadFile = File(...)):
    result = image_controller.upload_image(file)
    
    return CommonResponse.success_response(
        message="image_upload_success",
        result=result
    )
    