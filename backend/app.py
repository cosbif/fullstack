from fastapi import FastAPI
from routes.health import router as health_router
from routes.users import router as users_router
from routes.images import router as images_router
from database.database import Base, engine
import models.user
from routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CleanMyData API",
    description="API для анонимизации персональных данных на изображениях",
    version="0.1.0"
)

# Подключение маршрутов
app.include_router(health_router)
app.include_router(users_router)
app.include_router(images_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "CleanMyData backend is running"}
