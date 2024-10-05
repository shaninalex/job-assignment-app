from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

from pkg.settings import CONFIG

engine: AsyncEngine = create_async_engine(CONFIG.DATABASE_URI, echo=True)

async_session: AsyncSession = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


@web.middleware
async def db_session_middleware(request, handler):
    _session: AsyncSession = request.app.container.session
    async with _session() as session:
        try:
            response = await handler(request)
            await session.commit()
            return response
        except Exception as e:
            await session.rollback()
            raise e
