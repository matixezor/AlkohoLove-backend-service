from os import getenv
from httpx import AsyncClient
from pytest_asyncio import fixture
from asyncio import get_event_loop
from sqlalchemy.orm import sessionmaker
from typing import Callable, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


DATABASE_URL = getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    autocommit=False,
    expire_on_commit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


@fixture
async def db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.flush()
        await session.rollback()


@fixture
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session

    return _override_get_db


@fixture
async def async_client(override_get_db: Callable) -> AsyncGenerator:
    from src.database.database_config import get_db
    from src.main import app

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@fixture
async def user_token(async_client: AsyncClient) -> str:
    data = {
        'username': 'Adam_Skorupa',
        'password': 'JanJan123'
    }
    response = await async_client.post('/auth/token', data=data)
    return response.json()['access_token']


@fixture
async def admin_token(async_client: AsyncClient) -> str:
    data = {
        'username': 'admin',
        'password': 'JanJan123'
    }
    response = await async_client.post('/auth/token', data=data)
    return response.json()['access_token']


@fixture(scope='session')
def event_loop():
    loop = get_event_loop()
    yield loop
    loop.close()
