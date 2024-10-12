import asyncio

from sqlalchemy import text
from app.db.session import DatabaseSessionManager
from app.db.models import Base
from app.config import settings


async def main():
    db = DatabaseSessionManager(settings.database_url)
    async with db.connect() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())

