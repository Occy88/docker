from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select
from typing import Type, Generic, List, Optional, Callable, TypeVar
from sqlalchemy.orm import sessionmaker
import os
import json
T = TypeVar("T", bound=SQLModel)  # T is bound to SQLModel for tighter integration

from web.db import get_session
class CRUDBase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_multi(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[T]:
        result = await session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def get(self, session: AsyncSession, id: int) -> Optional[T]:
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def create(self, session: AsyncSession, obj_in: T) -> T:
        obj_in_data = obj_in.dict(exclude_unset=True)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, session: AsyncSession, id: int, obj_in: T) -> Optional[T]:
        db_obj = await session.get(self.model, id)
        if not db_obj:
            return None
        obj_in_data = obj_in.dict(exclude_unset=True)
        for key, value in obj_in_data.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id: int) -> Optional[T]:
        db_obj = await session.get(self.model, id)
        if db_obj:
            await session.delete(db_obj)
            await session.commit()
            return db_obj
        return None

def async_crud_router(model: Type[SQLModel], prefix: str,
                      enable_create: bool = True, enable_read: bool = True, enable_update: bool = True, enable_delete: bool = True) -> APIRouter:
    router = APIRouter()
    crud_service = CRUDBase(model)

    if enable_read:
        @router.get(f"/{prefix}", response_model=List[model])
        async def read_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
            return await crud_service.get_multi(db, skip=skip, limit=limit)

        @router.get(f"/{prefix}/{{id}}", response_model=model)
        async def read_item(id: int, db: AsyncSession = Depends(get_session)):
            item = await crud_service.get(db, id)
            if item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            return item

    # if enable_create:
    #     @router.post(f"/{prefix}", response_model=model, status_code=status.HTTP_201_CREATED)
    #     async def create_item(item: model, db: AsyncSession = Depends(get_session)):
    #         return await crud_service.create(db, item)

    if enable_update:
        @router.put(f"/{prefix}/{{id}}", response_model=model)
        async def update_item(id: int, item: model, db: AsyncSession = Depends(get_session)):
            updated_item = await crud_service.update(db, id, item)
            if updated_item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            return updated_item

    if enable_delete:
        @router.delete(f"/{prefix}/{{id}}", response_model=model)
        async def delete_item(id: int, db: AsyncSession = Depends(get_session)):
            deleted_item = await crud_service.delete(db, id)
            if deleted_item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            return deleted_item

    return router
