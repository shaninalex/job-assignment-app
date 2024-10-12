import pytest_asyncio
from sqlalchemy import text

from app.db.models import Base
from app.db.session import DatabaseSessionManager

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/application_test"


@pytest_asyncio.fixture
async def session():
    on_test = DatabaseSessionManager(DATABASE_URL)

    # Create tables before the test
    async with on_test.connect() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        await conn.run_sync(Base.metadata.create_all)

    enter = DatabaseSessionManager(DATABASE_URL)
    yield enter.session

    # Drop tables after the test to clean up
    async with on_test.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def connect():
    manager = DatabaseSessionManager(DATABASE_URL)
    return manager.connect
