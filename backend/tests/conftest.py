import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from pkg.settings import Config, Redis


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
