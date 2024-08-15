from sqlalchemy import create_engine
from database.models import Base

# models
import database.models.admin
import database.models.auth
import database.models.candidate
import database.models.company


def create_tables(database_uri, echo):
    engine = create_engine(database_uri, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
