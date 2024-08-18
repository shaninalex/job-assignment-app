from sqlalchemy.types import Boolean, Text
from datetime import datetime
from sqlalchemy import ForeignKey, func
from . import Base

from sqlalchemy import JSON, UUID, String, text
from sqlalchemy.orm import mapped_column, Mapped, relationship
import uuid


class Candidate(Base):
    __tablename__ = "candidate"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    settings: Mapped[JSON] = mapped_column(JSON, nullable=True)
    active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )
    confirmed: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )
    photo_link: Mapped[str] = mapped_column(Text, nullable=True)
    resume_link: Mapped[str] = mapped_column(Text, nullable=True)
    social_accounts: Mapped[JSON] = mapped_column(JSON, nullable=True)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    about_additional: Mapped[str] = mapped_column(Text, nullable=True)
    skills: Mapped[JSON] = mapped_column(JSON, nullable=True)
    certificates: Mapped[JSON] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )
    auth_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("auth.id"), unique=True, nullable=True
    )

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "settings": self.settings,
            "active": self.active,
            "confirmed": self.confirmed,
            "photo_link": self.photo_link,
            "resume_link": self.resume_link,
            "social_accounts": self.social_accounts,
            "about": self.about,
            "about_additional": self.about_additional,
            "skills": self.skills,
            "certificates": self.certificates,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class CandidateExperience(Base):
    __tablename__ = "candidate_experience"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    company_name: Mapped[str] = mapped_column(Text, nullable=True)
    company_link: Mapped[str] = mapped_column(Text, nullable=True)
    work_start: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), nullable=True
    )
    work_end: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), nullable=False
    )
    position: Mapped[str] = mapped_column(Text, nullable=True)
    responsibility: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    # candidate_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('candidate.id'), unique=True, nullable=True)
    # candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="candidate", uselist=False, cascade="all")
