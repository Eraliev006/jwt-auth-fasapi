from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DB_URL = 'postgresql+asyncpg://postgres:19871460@localhost:5432/project'



@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession]:
    async_engine = create_async_engine(DB_URL, echo=True, echo_pool=False, max_overflow=10, pool_size=5)
    AsyncTestingSession = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )
    async with AsyncTestingSession() as session:
        yield session
        await session.rollback()