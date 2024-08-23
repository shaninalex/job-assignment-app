import uuid
from datetime import datetime
from sqlalchemy import UUID, String, text, Text, Enum, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from . import Base
from .const import CompanyManagerRole
from typing import List


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
    managers: Mapped[List["CompanyManager"]
                     ] = relationship(back_populates="company")
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
        managers = []
        for m in self.managers:
            managers.append(m.json())

        return {
            "id": str(self.id),
            "name": self.name,
            "image_link": self.image_link,
            "managers": managers,
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
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), unique=True, nullable=True
    )

    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id"), unique=True, nullable=False
    )
    company: Mapped["Company"] = relationship(back_populates="managers")

    def json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "company": self.company.json(),
        }
