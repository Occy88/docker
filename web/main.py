from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from web.db import init_models, get_session
from web.models.user import User


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



@app.post("/users/", response_model=User,status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: AsyncSession = Depends(get_session)):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

