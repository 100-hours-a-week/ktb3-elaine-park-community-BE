from fastapi import UploadFile
from typing import Dict, Any
import shutil
import uuid
import os

from common import database

UPLOAD_DIR = "uploaded_images"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
def upload_image(file: UploadFile) -> Dict[str, Any]:
    file_extension = os.path.splitext(file.filename)[1]
    saved_filename = f"{uuid.uuid4()}{file_extension}"
    
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    new_image = {
        "imageId" : database.NEXT_IMAGE_ID,
        "originalName" : file.filename,
        "storedName" : saved_filename,
        "url" : f"/images/{saved_filename}"
    }
    
    database.IMAGE_DB.append(new_image)
    database.NEXT_IMAGE_ID += 1
    
    return new_image