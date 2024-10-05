import uuid
from datetime import datetime, timedelta
from typing import List

from sqlalchemy import (
    JSON,
    String,
    UUID,
    text,
    Text,
    ForeignKey,
    func,
    Enum,
    Boolean,
    VARCHAR,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from pkg.consts import (
    Remote,
    SalaryType,
    WorkingHours,
    TravelRequired,
    PositionStatus,
    AuthStatus,
    Role,
    ConfirmStatusCode,
)
from pkg.database import Base


class Staff(Base):
    __tablename__ = "admin_staff"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    def json(self):
        return {"id": str(self.id), "name": self.name, "email": self.email}


class Candidate(Base):
    __tablename__ = "candidate"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    resume_link: Mapped[str] = mapped_column(Text, nullable=True)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    about_additional: Mapped[str] = mapped_column(Text, nullable=True)
    skills: Mapped[JSON] = mapped_column(JSON, nullable=True)
    certificates: Mapped[JSON] = mapped_column(JSON, nullable=True)
    experiences: Mapped[List["CandidateExperience"]] = relationship(back_populates="candidate", uselist=True)

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), unique=True, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="candidate")

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
    work_start: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
    work_end: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=False)
    position: Mapped[str] = mapped_column(Text, nullable=True)
    responsibility: Mapped[str] = mapped_column(Text, nullable=True)
    candidate: Mapped["Candidate"] = relationship(back_populates="experiences")
    candidate_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidate.id"), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
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
            "work_start": str(self.work_start),
            "work_end": str(self.work_end),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class Company(Base):
    __tablename__ = "company"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    name: Mapped[str] = mapped_column(String(30), unique=True)
    image_link: Mapped[str] = mapped_column(Text, nullable=True)
    managers: Mapped[List["CompanyManager"]] = relationship("CompanyManager", back_populates="company")
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    # NOTE:
    # company_rating ??

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "image_link": self.image_link,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class CompanyManager(Base):
    __tablename__ = "company_manager"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), unique=True, nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="manager")
    company_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("company.id"), unique=True, nullable=False)
    company: Mapped["Company"] = relationship("Company", back_populates="managers")

    def json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "company_id": str(self.company_id),
        }


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    responsibilities: Mapped[str] = mapped_column(Text)
    requirements: Mapped[str] = mapped_column(Text)
    interview_stages: Mapped[str] = mapped_column(Text)
    offer: Mapped[str] = mapped_column(Text)
    remote: Mapped[Remote] = mapped_column(Enum(Remote))
    salary: Mapped[SalaryType] = mapped_column(Enum(SalaryType))
    hours: Mapped[WorkingHours] = mapped_column(Enum(WorkingHours))
    travel: Mapped[TravelRequired] = mapped_column(Enum(TravelRequired))
    status: Mapped[PositionStatus] = mapped_column(Enum(PositionStatus))
    price_range: Mapped[str] = mapped_column(VARCHAR(50))

    company_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("company.id"), nullable=False)

    # NOTE: column ideas
    # - search_tags
    # - featured/important

    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    def json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "responsibilities": self.responsibilities,
            "requirements": self.requirements,
            "interview_stages": self.interview_stages,
            "offer": self.offer,
            "remote": str(self.remote.value),
            "salary": str(self.salary.value),
            "hours": str(self.hours.value),
            "travel": str(self.travel.value),
            "status": str(self.status.value),
            "price_range": str(self.price_range),
            "company_id": str(self.company_id),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class PositionViews(Base):
    """PositionViews tracking.
    Since positions is public we views can by or not made by authorized account.
    That's why user_is nullable=True"""

    __tablename__ = "positions_views"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )

    position_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("positions.id"))
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)

    def json(self):
        return {
            "id": str(self.id),
            "position_id": str(self.position_id),
            "user_id": str(self.user_id),
            "created_at": str(self.created_at),
        }


class PositionFeedback(Base):
    __tablename__ = "positions_feedbacks"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    position_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("positions.id"))
    message: Mapped[Text] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="feedbacks")

    def json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "position_id": str(self.position_id),
            "message": self.message,
            "created_at": str(self.created_at),
        }


class User(Base):
    __tablename__ = "user"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(VARCHAR(100), unique=True)
    settings: Mapped[JSON] = mapped_column(JSON, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"))
    image: Mapped[str] = mapped_column(Text, nullable=True)
    social_accounts: Mapped[JSON] = mapped_column(JSON, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
    status: Mapped[AuthStatus] = mapped_column(Enum(AuthStatus), default=AuthStatus.PENDING)
    role: Mapped[Role] = mapped_column(Enum(Role))
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    codes: Mapped[List["ConfirmCode"]] = relationship("ConfirmCode", back_populates="user")
    feedbacks: Mapped[List["PositionFeedback"]] = relationship("PositionFeedback", back_populates="user")
    manager: Mapped["CompanyManager"] = relationship("CompanyManager", back_populates="user")
    candidate: Mapped["User"] = relationship("Candidate", back_populates="user")

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "settings": self.settings,
            "active": self.active,
            "image": self.image,
            "social_accounts": self.social_accounts,
            "confirmed": self.confirmed,
            "status": str(self.status.value),
            "role": self.role.name,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


def default_expired_at():
    # Compute the default expiration time as `datetime.now() + 5 minutes`
    return datetime.now() + timedelta(minutes=5)


class ConfirmCode(Base):
    __tablename__ = "confirm_codes"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    code: Mapped[str] = mapped_column(VARCHAR(6))
    status: Mapped[ConfirmStatusCode] = mapped_column(Enum(ConfirmStatusCode), default=ConfirmStatusCode.SENT)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now())
    expired_at: Mapped[datetime] = mapped_column(default=default_expired_at)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="codes")

    def json(self):
        return {
            "id": str(self.id),
            "code": self.code,
            "status": self.status.name,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "expired_at": str(self.expired_at),
            "user_id": str(self.user_id),
        }
