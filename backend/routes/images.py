import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.schemas import ProcessedImageCreate, ProcessedImageOut
from services.image_service import create_processed_image, get_images_by_user, save_uploaded_image
from services.token_utils import get_current_user_id
from fastapi.responses import FileResponse
from models.processed_image import ProcessedImage

router = APIRouter(prefix="/images", tags=["Images"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProcessedImageOut)
def add_processed_image(
    item: ProcessedImageCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return create_processed_image(db, user_id, item)



@router.get("/", response_model=list[ProcessedImageOut])
def list_images(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return get_images_by_user(db, user_id)

@router.post("/upload")
def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return save_uploaded_image(db, user_id, file)

@router.get("/download/{image_id}")
def download_image(image_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    image = db.query(ProcessedImage).filter(ProcessedImage.id == image_id, ProcessedImage.user_id == user_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = image.processed_path
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(file_path, filename=os.path.basename(file_path))

@router.delete("/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    image = db.query(ProcessedImage).filter(ProcessedImage.id == image_id, ProcessedImage.user_id == user_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # удаляем файлы
    for path in [image.original_path, image.processed_path]:
        if os.path.isfile(path):
            os.remove(path)

    # удаляем запись из БД
    db.delete(image)
    db.commit()

    return {"detail": "Image deleted successfully"}