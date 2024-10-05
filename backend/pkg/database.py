import aiohttp_sqlalchemy
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def create_session(db_url: str):
    eng = create_async_engine(db_url, echo=True)
    session = AsyncSession(bind=eng, expire_on_commit=False)
    return eng, session


@web.middleware
async def db_session_middleware(request, handler):
    async with aiohttp_sqlalchemy.get_session(request) as session:
        try:
            response = await handler(request)
            await session.commit()
            return response
        except Exception as e:
            await session.rollback()
            raise e
