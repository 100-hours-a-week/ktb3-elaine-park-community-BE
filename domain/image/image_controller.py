from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import Dict, Any
import shutil
import uuid
import os
from . import image_model

UPLOAD_DIR = "uploaded_images"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
def upload_image(db: Session, file: UploadFile) -> image_model.Image:
    file_extension = os.path.splitext(file.filename)[1]
    saved_filename = f"{uuid.uuid4()}{file_extension}"
    
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    
    # 컴터 하드디스크에 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    new_image = image_model.Image(
        originalName = file.filename,
        storedName = saved_filename,
        url = f"/images/{saved_filename}"
    )
    
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    
    return new_image