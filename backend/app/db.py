import enum
from datetime import datetime
from typing import List
from sqlalchemy import String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import functions


class Base(DeclarativeBase):
    pass


class Role(enum.Enum):
    admin = 1
    manager = 2


class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    skills: Mapped[List["Skill"]] = relationship(cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    phone: Mapped[str] = mapped_column(String(30))
    about: Mapped[str] = mapped_column(String(250))
    submitted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.now(),
                                            nullable=False,
                                            server_default=functions.now())

    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    position: Mapped["Position"] = relationship(cascade="all, delete-orphan")


candidates_skills: Table = Table(
    'candidates_skills',
    meta,
    Column("candidate_id", Integer, ForeignKey(
        "candidates.id"), nullable=False),
    Column("skill", Integer, ForeignKey("skills.id"), nullable=False),
)

position_skills: Table = Table(
    'position_skills',
    meta,
    Column("position_id", Integer, ForeignKey(
        "position.id"), nullable=False),
    Column("skill", Integer, ForeignKey("skills.id"), nullable=False),
)

users: Table = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True, index=True),
    Column('email', Text, unique=True, nullable=False),
    Column('password', Text, nullable=False),
    Column('role', Enum(Role), default=Role.manager.name, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.now(),
           nullable=False, server_default=functions.now()),
)

candidates_submittions: Table = Table(
    'candidates_submittions',
    meta,
    Column('id', Integer, primary_key=True, index=True),
    Column("candidate_id", Integer, ForeignKey(
        "candidates.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column('submitted', Boolean, default=False),
    Column('reason', Text),
    Column('created_at', TIMESTAMP, default=datetime.now(),
           nullable=False, server_default=functions.now()),
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


def create_tables(database_uri, echo):
    engine = create_engine(database_uri, echo=echo)
    meta.create_all(engine)


async def db_context(app):
    engine = await aiopg.sa.create_engine(
        dsn=app['config']['DATABASE_URL'],
        echo=False,
        # echo=app['config']['DEBUG'],
    )

    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
