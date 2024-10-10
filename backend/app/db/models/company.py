from datetime import datetime
from typing import List

from sqlalchemy import Enum, String, Text, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import Base
from app.enums import CompanyStatus, CompanyMemberStatus


class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    website: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    image_link: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[CompanyStatus] = mapped_column(Enum(CompanyStatus))
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    positions: Mapped[List["Position"]] = relationship(  # type: ignore # noqa
        "Position", back_populates="company", lazy="noload"
    )
    members: Mapped[List["CompanyMember"]] = relationship(  # type: ignore # noqa
        "CompanyMember", back_populates="company", lazy="noload"
    )


class CompanyMember(Base):
    __tablename__ = "company_member"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True, nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="member")
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), unique=True, nullable=False)
    company: Mapped["Company"] = relationship("Company", back_populates="members")
    status: Mapped[CompanyMemberStatus] = mapped_column(Enum(CompanyMemberStatus), default=CompanyMemberStatus.ACTIVE)
