from datetime import datetime
import enum

import aiopg.sa
from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    TIMESTAMP,
    Table,
    Text,
    VARCHAR,
    create_engine,
)
from sqlalchemy.sql import functions

meta = MetaData()


class Role(enum.Enum):
    admin = 1
    manager = 2


position: Table = Table(
    'position',
    meta,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', Text, nullable=False, unique=True),
    Column('description', Text, nullable=False, unique=True),
)

candidates: Table = Table(
    'candidates',
    meta,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', Text, nullable=False),
    Column('email', Text, nullable=False),
    Column('phone', Text),
    Column('about', Text),
    Column('submitted', Boolean, default=False),
    Column("position_id", Integer, ForeignKey("position.id"), nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.now(),
           nullable=False, server_default=functions.now()),
)

skills: Table = Table(
    'skills',
    meta,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', VARCHAR(15), index=True, unique=True),
)

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

candidates_skills: Table = Table(
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
