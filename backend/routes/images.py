from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.schemas import ProcessedImageCreate, ProcessedImageOut
from services.image_service import create_processed_image, get_images_by_user

router = APIRouter(prefix="/images", tags=["Images"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProcessedImageOut)
def add_processed_image(item: ProcessedImageCreate, db: Session = Depends(get_db)):
    return create_processed_image(db, item)


@router.get("/{user_id}", response_model=list[ProcessedImageOut])
def list_images(user_id: int, db: Session = Depends(get_db)):
    return get_images_by_user(db, user_id)
