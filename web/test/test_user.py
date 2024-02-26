# tests/test_user_crud.py
from datetime import datetime, timezone
import uuid
import pytz
import pytest
from fastapi import Depends
from httpx import AsyncClient
from pydantic import BaseModel
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
    created_at =datetime.now(pytz.timezone('Europe/London'))
    updated_at=datetime.now(pytz.timezone('Europe/London'))
    date_chosen= datetime.now(pytz.timezone('Europe/London'))
    id = uuid.uuid4()
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession = Depends(get_session)):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        instance = UserFactory.build()
        js=instance.model_dump(mode="json")
        js.pop('updated_at')
        js.pop('created_at')
        response = await ac.post("/users/", json=js)
        assert response.status_code == status.HTTP_201_CREATED,response.json()
        assert response.json()["email"] == instance.email

class SimpleModel(BaseModel):
    date_value: datetime


def test_simple_model_date_parsing():
    # Create a dictionary with a datetime string
    input_data = {"date_value":datetime.now().isoformat()}

    # Instantiate the SimpleModel with the dictionary
    model_instance = SimpleModel(**input_data)

    # Assert that the date_value field is correctly converted to a datetime object
    assert isinstance(model_instance.date_value, datetime)