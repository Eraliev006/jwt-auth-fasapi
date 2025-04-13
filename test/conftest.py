from typing import AsyncGenerator, Generator

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from starlette.background import BackgroundTasks
from starlette.testclient import TestClient

from app.main import app
from test.utils.utils import random_email, random_lower_string

DB_URL = 'postgresql+asyncpg://postgres:19871460@localhost:5432/project'



@pytest.fixture
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

@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope='function')
def fake_login_user_data() -> dict:
    fake_login_user_data = {
        'email': random_email(),
        'password': random_lower_string()
    }
    return fake_login_user_data

@pytest.fixture(scope='function')
def background_tasks():
    return BackgroundTasks()