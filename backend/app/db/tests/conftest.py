import pytest_asyncio

from app.db.session import DatabaseSessionManager

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/application_test"


@pytest_asyncio.fixture
async def session():
    manager = DatabaseSessionManager(DATABASE_URL)
    return manager.session


@pytest_asyncio.fixture
async def connect():
    manager = DatabaseSessionManager(DATABASE_URL)
    return manager.connect
