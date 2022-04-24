from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.config import DATABASE_URL


async def get_db():
    async with async_session() as session:
        yield session
        await session.commit()


engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(
    autocommit=False,
    expire_on_commit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)
