import logging
import sys

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from pkg.settings import Config, Redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

config: Config = Config(
    DATABASE_URI="postgresql+asyncpg://postgres:postgres@localhost:5432/application_test",
    DEBUG=True,
    APP_PORT=8000,
    RABBIT_URL="amqp://guest:guest@localhost/",
    REDIS=Redis(
        REDIS_HOST="localhost",
        REDIS_PORT=6379,
        REDIS_DB=0,
    ),
    APP_SECRET="test_jwt_token",
)

_engine: AsyncEngine = create_async_engine(config.DATABASE_URI, echo=True)
_async_session: AsyncSession = sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="module")
def test_config() -> Config:
    return config


@pytest.fixture(scope="module")
def async_engine() -> AsyncEngine:
    return _engine


@pytest.fixture(scope="module")
def async_session() -> AsyncSession:
    return _async_session


@pytest.fixture
async def cleanup():
    yield
    await db_cleanup()


async def db_cleanup():
    engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/application_test", echo=False)
    async with engine.begin() as conn:
        for table in ["positions", "company_manager", "company", "confirm_codes", "user"]:
            await conn.execute(text(f"""DELETE FROM "{table}";"""))
    logger.info("Database tables cleaned up")
