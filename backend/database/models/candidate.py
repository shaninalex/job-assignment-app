import uuid
from datetime import datetime
from sqlalchemy import JSON, UUID, text, ForeignKey, func
from sqlalchemy.types import Text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from typing import List, Optional
from . import Base


class Candidate(Base):
    __tablename__ = "candidate"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    resume_link: Mapped[str] = mapped_column(Text, nullable=True)
    social_accounts: Mapped[JSON] = mapped_column(JSON, nullable=True)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    about_additional: Mapped[str] = mapped_column(Text, nullable=True)
    skills: Mapped[JSON] = mapped_column(JSON, nullable=True)
    certificates: Mapped[JSON] = mapped_column(JSON, nullable=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), unique=True, nullable=True
    )

    experiences: Mapped[Optional[List["CandidateExperience"]]] = relationship(
        back_populates="candidate", uselist=True
    )

    def json(self):
        return {
            "resume_link": self.resume_link,
            "about": self.about,
            "about_additional": self.about_additional,
            "skills": self.skills,
            "certificates": self.certificates,
            "experiences": [e.json() for e in self.experiences],
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
    candidate: Mapped["Candidate"] = relationship(back_populates="experiences")
    candidate_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidate.id"), unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    def json(self):
        return {
            "id": str(self.id),
            "company_name": self.company_name,
            "company_link": self.company_link,
            "position": self.position,
            "responsibility": self.responsibility,
            "candidate": self.candidate.json(),
            "work_start": str(self.work_start),
            "work_end": str(self.work_end),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
