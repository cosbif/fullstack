from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class ProcessedImageCreate(BaseModel):
    user_id: int
    original_path: str
    processed_path: str


class ProcessedImageOut(BaseModel):
    id: int
    user_id: int
    original_path: str
    processed_path: str

    class Config:
        orm_mode = True
