# tests/test_user_crud.py
import datetime
import uuid
import pytz
import pytest
from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
# tests/factories.py
from fastapi import status
import factory

from web.db import get_session
from web.models.user import User
from web.main import app
class UserFactory(factory.Factory):
    class Meta:
        model = User
    created=t = datetime.datetime.now(tz=pytz.timezone('Europe/Warsaw'))
    modified=t = datetime.datetime.now(tz=pytz.timezone('Europe/Warsaw'))
    id = uuid.uuid4()
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession = Depends(get_session)):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        instance = UserFactory.build()
        response = await ac.post("/users/", json=instance.model_dump(mode="json"))
        assert response.status_code == status.HTTP_201_CREATED,response.json()
        assert response.json()["email"] == instance.email
        # Additional assertions as necessary
#
# @pytest.mark.asyncio
# async def test_update_user(db_session: AsyncSession = Depends(get_session)):
#     user = UserFactory.create()  # Create a user to update
#     db_session.add(user)-
#     await db_session.commit()
#
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         updated_data = {"username": "new_username"}
#         response = await ac.put(f"/users/{user.id}", json=updated_data)
#         assert response.status_code == 200
#         data = response.json()
#         assert data["username"] == "new_username"
#         # Additional assertions as necessary
#
# @pytest.mark.asyncio
# async def test_delete_user(db_session: AsyncSession = Depends(get_session)):
#     user = UserFactory.create()  # Create a user to delete
#     db_session.add(user)
#     await db_session.commit()
#
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.delete(f"/users/{user.id}")
#         assert response.status_code == 200
#         # Check if the user is actually deleted, potentially querying the database
#
# # Add tests for PATCH and other operations as needed, following the pattern above.
