from sqlalchemy.orm import Session
from models.processed_image import ProcessedImage
from models.schemas import ProcessedImageCreate


def create_processed_image(db: Session, item: ProcessedImageCreate):
    db_item = ProcessedImage(
        user_id=item.user_id,
        original_path=item.original_path,
        processed_path=item.processed_path
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_images_by_user(db: Session, user_id: int):
    return db.query(ProcessedImage).filter(ProcessedImage.user_id == user_id).all()
