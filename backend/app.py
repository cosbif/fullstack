from fastapi import FastAPI
from routes.health import router as health_router

app = FastAPI(
    title="CleanMyData API",
    description="API для анонимизации персональных данных на изображениях",
    version="0.1.0"
)

# Подключение маршрутов
app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "CleanMyData backend is running"}
