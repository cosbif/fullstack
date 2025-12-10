from sqlalchemy.orm import Session
from models.user import User
from models.schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    hashed_pwd = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
