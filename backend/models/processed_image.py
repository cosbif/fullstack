from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database.database import Base

class ProcessedImage(Base):
    __tablename__ = "processed_images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    original_path = Column(String)      # путь к исходному фото
    processed_path = Column(String)     # путь к обработанному фото
    created_at = Column(DateTime(timezone=True), server_default=func.now())
