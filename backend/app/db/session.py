import contextlib
from collections.abc import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine, AsyncConnection

from app.config import settings
from app.exceptions.exceptions import ServiceError


# thx Arjan :)


class DatabaseSessionManager:
    def __init__(self, host: str):
        # NOTE: create_async_engine require connect_args={"check_same_thread": False} only if you use sqlite+aiosqlite:///
        # database. Because it's file based db. For postgresql+asyncpg:// this check is not needed.
        self.engine: AsyncEngine | None = create_async_engine(host, echo=False)
        self._sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(autocommit=False, bind=self.engine)

    async def close(self):
        if self.engine is None:
            raise ServiceError("Engine not initialized", name="DB")
        await self.engine.dispose()
        self.engine = None
        self._sessionmaker = None  # type: ignore

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise ServiceError("Engine not initialized", name="DB")

        async with self.engine.begin() as connection:
            try:
                yield connection
            except SQLAlchemyError as e:
                await connection.rollback()
                raise ServiceError(message=parse_db_error_text(e.args[0]), name="DB")

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self._sessionmaker:
            raise ServiceError("Sessionmaker not initialized")

        session = self._sessionmaker()
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise ServiceError(message=parse_db_error_text(e.args[0]), name="DB")
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.database_url)


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


def parse_db_error_text(error_text: str) -> str:
    parts = error_text.split("DETAIL:  Key ")
    if len(parts) > 1:
        return parts[1]
    return error_text
