from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.health import router as health_router
from routes.users import router as users_router
from routes.images import router as images_router
from database.database import Base, engine
from routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def root():
    return {"message": "CleanMyData backend is running"}
