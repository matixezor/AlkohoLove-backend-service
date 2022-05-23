from os import environ
from httpx import AsyncClient
from pytest_asyncio import fixture
from typing import Callable, AsyncGenerator

from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler


@fixture(autouse=True)
def mock_settings_env_vars():
    from unittest import mock
    with mock.patch.dict(environ, {'STATIC_DIR': '../../static'}):
        yield


@fixture
def override_get_db(mongodb) -> Callable:
    def _override_get_db():
        AlcoholDatabaseHandler.update_validation(mongodb)
        return mongodb

    return _override_get_db


@fixture
async def async_client(override_get_db: Callable) -> AsyncGenerator:
    from src.infrastructure.database.database_config import get_db
    from src.main import app

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@fixture
async def user_token_headers(async_client: AsyncClient) -> dict[str, str]:
    data = {
        'username': 'Adam_Skorupa',
        'password': 'JanJan123'
    }
    response = await async_client.post('/auth/token', data=data)
    return {
        'Authorization': f"Bearer {response.json()['access_token']}"
    }


@fixture
async def admin_token_headers(async_client: AsyncClient) -> dict[str, str]:
    data = {
        'username': 'admin',
        'password': 'JanJan123'
    }
    response = await async_client.post('/auth/token', data=data)
    return {
        'Authorization': f"Bearer {response.json()['access_token']}"
    }
