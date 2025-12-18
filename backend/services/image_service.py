import os
import shutil
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models.processed_image import ProcessedImage
from models.schemas import ProcessedImageCreate
from services.ml_service import anonymize_image

UPLOAD_DIR = "uploads"
ORIGINALS_DIR = os.path.join(UPLOAD_DIR, "originals")
PROCESSED_DIR = os.path.join(UPLOAD_DIR, "processed")

os.makedirs(ORIGINALS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def create_processed_image(db: Session, user_id: int, item: ProcessedImageCreate):
    db_item = ProcessedImage(
        user_id=user_id,
        original_path=item.original_path,
        processed_path=item.processed_path
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_images_by_user(db: Session, user_id: int):
    return db.query(ProcessedImage).filter(ProcessedImage.user_id == user_id).all()

def save_uploaded_image(db: Session, user_id: int, file: UploadFile):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"

    original_path = os.path.join(ORIGINALS_DIR, filename)
    processed_path = os.path.join(PROCESSED_DIR, filename)  # пока копия

    with open(original_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    anonymize_image(original_path, processed_path)
    
    db_item = ProcessedImage(
        user_id=user_id,
        original_path=original_path,
        processed_path=processed_path,
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {
        "id": db_item.id,
        "original_path": original_path,
        "processed_path": processed_path,
    }