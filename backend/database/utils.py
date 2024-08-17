import os
from alembic import command, config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine

from database.models import Base


def create_tables(database_uri, echo):
    engine = create_engine(database_uri, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def database_url():
    return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
        os.getenv("DB_USERNAME"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("DB_NAME"),
    )


def check_migrations():
    alembic_cfg = config.Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)
    head_revision = script.get_current_head()
    command.upgrade(alembic_cfg, str(head_revision))
    print(f"Last database schema version: {head_revision}\n")
