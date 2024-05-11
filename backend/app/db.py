import aiopg.sa
from datetime import datetime
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Text,
    TIMESTAMP,
    Integer,
    ForeignKey,
    Boolean,
    VARCHAR
)
from sqlalchemy.sql import functions

meta = MetaData()

log = Table(
    'log',
    meta,
    Column('id', Integer, primary_key=True, index=True),
    Column('text', Text),
    Column('created_at', TIMESTAMP, default=datetime.now(),
           nullable=False, server_default=functions.now()),
)

position = Table(
    'position',
    meta,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', Text, nullable=False, unique=True),
    Column('description', Text, nullable=False, unique=True),
    # TODO: skills required
)

candidates = Table(
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

skills = Table(
    'skills',
    meta,
    Column('name', VARCHAR(15), primary_key=True, index=True, unique=True),
)

candidates_skills = Table(
    'candidates_skills',
    meta,
    Column("candidate_id", Integer, ForeignKey(
        "candidates.id"), nullable=False),
    Column("skill", Text, ForeignKey("skills.name"), nullable=False),
)

user = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True, index=True),
    Column('email', Text, unique=True, nullable=False),
    Column('password', Text, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.now(),
           nullable=False, server_default=functions.now()),
)

candidates_skills = Table(
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
        echo=app['config']['DEBUG'])

    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
