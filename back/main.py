import enum
import uuid
import os
import asyncio
from datetime import datetime
from sqlalchemy import UUID, String, text, Text, JSON, Boolean, ForeignKey, func, VARCHAR, Enum, select
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
from dotenv import load_dotenv

load_dotenv(BASE_DIR / ".env")


def database_url():
    return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
        os.getenv('DB_USERNAME'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_NAME'),
    )

class AuthStatus(enum.Enum):
    ACTIVE = 'active'
    BANNED = 'banned'
    PENDING = 'pending'


class Base(DeclarativeBase):
    pass


class Staff(Base):
    __tablename__ = "admin_staff"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("uuid_generate_v4()"))
    name: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100), unique=True)



async def async_main() -> None:
    engine = create_async_engine(database_url(), echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        session.add_all(
            [
                Staff(name="test", email="test@test.com", password="329847324"),
            ]
        )

        await session.commit()

    
asyncio.run(async_main())