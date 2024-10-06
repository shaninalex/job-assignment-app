import asyncio
import logging
import sys
import time
import pytest
from sqlalchemy import create_engine, text, delete
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from api.main import api_factory
from pkg.settings import Config, Redis
from pkg.models.models import CompanyManager, Company, ConfirmCode, User, Position  # Import your models

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
_async_session_factory = sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="function")
async def async_session() -> AsyncSession:  # type: ignore
    async with _async_session_factory() as session:
        yield session
        await session.rollback()  # Ensure rollback after each test for isolation


@pytest.fixture(scope="function")
def test_config() -> Config:
    return config


@pytest.fixture(scope="function")
async def aiohttp_client_instance(aiohttp_client, test_config):
    app = await api_factory(test_config)
    client = await aiohttp_client(app)
    yield client
    await client.close()


async def db_cleanup():
    logger.info("Database tables clear start")
    engine = create_async_engine(config.DATABASE_URI, echo=False)
    async with engine.begin() as conn:
        for table in ["positions", "company_manager", "company", "confirm_codes", "user"]:
            await conn.execute(text(f"""DELETE FROM "{table}";"""))
    logger.info("Done")


def pytest_sessionfinish(session, exitstatus):
    time.sleep(2)
    asyncio.run(db_cleanup())
