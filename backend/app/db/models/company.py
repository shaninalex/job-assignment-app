from typing import List
import uuid

from sqlalchemy import UUID, Enum, String, Text, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import Base
from app.db.models.utils import CreatedUpdatedFields
from app.enums import CompanyStatus, CompanyMemberStatus


class Company(Base, CreatedUpdatedFields):
    __tablename__ = "company"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    name: Mapped[str] = mapped_column(String(100), unique=True)
    website: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    image_link: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[CompanyStatus] = mapped_column(Enum(CompanyStatus))

    positions: Mapped[List["Position"]] = relationship(  # type: ignore # noqa
        "Position", back_populates="company", lazy="noload"
    )
    members: Mapped[List["CompanyMember"]] = relationship(  # type: ignore # noqa
        "CompanyMember", back_populates="company", lazy="noload"
    )


class CompanyMember(Base, CreatedUpdatedFields):
    __tablename__ = "company_member"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), unique=True, nullable=True)
    company_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("company.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="member")  # type: ignore
    status: Mapped[CompanyMemberStatus] = mapped_column(Enum(CompanyMemberStatus), default=CompanyMemberStatus.ACTIVE)
    company: Mapped["Company"] = relationship("Company", back_populates="members")
