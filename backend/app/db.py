import enum
from datetime import datetime
from typing import List
from sqlalchemy import (
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    Enum,
    create_engine,
    Integer,
)
from sqlalchemy.sql import functions
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)

from app.settings import DATABASE_URI


class Base(DeclarativeBase):
    pass


class Role(enum.Enum):
    admin = 1
    manager = 2


class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    skills: Mapped[List["PositionSkill"]] = relationship(
        back_populates="position", cascade="all, delete-orphan"
    )

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "skills": [s.skill.json() for s in self.skills],
        }


class PositionSkill(Base):
    __tablename__ = "position_skills"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_id: Mapped[int] = mapped_column(Integer, ForeignKey("skills.id"))
    skill: Mapped["Skill"] = relationship("Skill", back_populates="positions")
    position_id: Mapped[int] = mapped_column(Integer, ForeignKey("positions.id"))
    position: Mapped["Position"] = relationship("Position", back_populates="skills")


class Candidate(Base):
    __tablename__ = "candidates"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    phone: Mapped[str] = mapped_column(String(30), unique=True)
    about: Mapped[str] = mapped_column(String(250))
    submitted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        default=datetime.now(),
        nullable=False,
        server_default=functions.now(),
    )

    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    position: Mapped["Position"] = relationship(cascade="all")
    skills: Mapped[List["CandidateSkill"]] = relationship(
        back_populates="candidate", cascade="all, delete-orphan"
    )
    secret: Mapped[str] = mapped_column(String, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "about": self.about,
            "submitted": self.submitted,
            "secret": self.secret,
            "created_at": str(self.created_at),
            "position": self.position.json(),
            "skills": [s.skill.json() for s in self.skills],
        }


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    skill: Mapped["Skill"] = relationship("Skill", back_populates="candidate")
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"))
    candidate: Mapped["Candidate"] = relationship(back_populates="skills")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(
        Enum(Role), default=Role.manager.name, nullable=False
    )
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        default=datetime.now(),
        nullable=False,
        server_default=functions.now(),
    )

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.name,
            "created_at": str(self.created_at),
        }


class CandidateSubmissions(Base):
    __tablename__ = "candidates_submissions"
    id: Mapped[int] = mapped_column(primary_key=True)
    submitted: Mapped[bool] = mapped_column(Boolean, default=False)
    reason: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP,
        default=datetime.now(),
        nullable=False,
        server_default=functions.now(),
    )
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)


Skill.candidate = relationship("CandidateSkill", back_populates="skill")
Skill.positions = relationship("PositionSkill", back_populates="skill")


class RecordNotFound(Exception):
    """Requested record in database was not found"""


def create_tables(database_uri, echo):
    engine = create_engine(database_uri, echo=echo)
    Base.metadata.create_all(engine)


async def db_context(app):
    # TODO: use async engine instead
    # https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/async_orm.html
    engine = create_engine(DATABASE_URI, echo=False)
    with Session(engine) as session:
        app["db"] = session
        yield
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
