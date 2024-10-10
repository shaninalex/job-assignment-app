import pytest
from sqlalchemy import text

from app.db.models import Base


@pytest.mark.asyncio
async def test_session_creation(session):
    assert session is not None


@pytest.mark.asyncio
async def test_is_connected(session):
    async with session() as session:
        await session.execute(text("SELECT 1"))


@pytest.mark.asyncio
async def test_create_tables(connect):
    async with connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
