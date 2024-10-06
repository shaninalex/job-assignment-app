import logging
import sys

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from api.main import api_factory

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

_engine: AsyncEngine = create_async_engine(config.DATABASE_URI, echo=False)
# _async_session: AsyncSession = sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="function")
def test_config() -> Config:
    # Create a fresh config for each test
    return config


@pytest.fixture(scope="function")
def async_engine() -> AsyncEngine:
    # Return a fresh async engine for each test
    return _engine


@pytest.fixture
async def test_app(test_config):
    return await api_factory(test_config)


@pytest.fixture(scope="function")
async def async_session(async_engine: AsyncEngine) -> AsyncSession: # type: ignore
    # Create a new async session per test
    async with AsyncSession(async_engine) as session:
        yield session
        await session.rollback()


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
