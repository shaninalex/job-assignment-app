import pytest_asyncio

from app.db.models import Base
from app.db.session import DatabaseSessionManager

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/application_test"


@pytest_asyncio.fixture
async def session():
    on_test = DatabaseSessionManager(DATABASE_URL)
    enter = DatabaseSessionManager(DATABASE_URL)
    yield enter.session

    # Drop tables after the test to clean up
    async with on_test.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest_asyncio.fixture
async def connect():
    manager = DatabaseSessionManager(DATABASE_URL)
    return manager.connect
