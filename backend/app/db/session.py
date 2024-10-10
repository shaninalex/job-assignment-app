import contextlib
from collections.abc import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine, AsyncConnection


class ServiceError(Exception):
    pass


class DatabaseSessionManager:
    def __init__(self, host: str):
        # NOTE: create_async_engine require connect_args={"check_same_thread": False} only if you use sqlite+aiosqlite:///
        # database. Because it's file based db. For postgresql+asyncpg:// this check is not needed.
        self.engine: AsyncEngine | None = create_async_engine(host, echo=False)
        self._sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(autocommit=False, bind=self.engine)

    async def close(self):
        if self.engine is None:
            raise ServiceError("Engine not initialized")
        await self.engine.dispose()
        self.engine = None
        self._sessionmaker = None  # type: ignore

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise ServiceError("Engine not initialized")

        async with self.engine.begin() as connection:
            try:
                yield connection
            except SQLAlchemyError as e:
                await connection.rollback()
                # logger.error(f"Connection error occurred: {e}")
                raise ServiceError("Connection error")

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self._sessionmaker:
            # logger.error("Sessionmaker is not available")
            raise ServiceError("Sessionmaker not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            # logger.error(f"Session error occurred: {e}")
            raise ServiceError("Session error")
        finally:
            await session.close()
