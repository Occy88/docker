from fastapi import FastAPI
from pydantic_settings import BaseSettings
from fastapi import status

from web.db import init_models


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str = "awsome_email"
    items_per_user: int = 50


settings = Settings()
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_models()



@app.get("/health")
async def health():
    return status.HTTP_200_OK