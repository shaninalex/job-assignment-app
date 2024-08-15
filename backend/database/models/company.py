from datetime import datetime
from sqlalchemy import ForeignKey, func
from . import Base
from .auth import Auth

from sqlalchemy import UUID, String, text
from sqlalchemy.orm import mapped_column, Mapped, relationship
import uuid


class Company(Base):
    __tablename__ = "company"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("uuid_generate_v4()"))
    name: Mapped[str] = mapped_column(String(30), unique=True)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class CompanyManager(Base):
    __tablename__ = "company_manager"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("uuid_generate_v4()"))
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), 
        server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), 
        server_default=func.now(),
        onupdate=func.now(), nullable=True
    )

    auth_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('auth.id'), unique=True, nullable=True)
    auth: Mapped["Auth"] = relationship("Auth", back_populates="candidate", uselist=False)

    company_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('company.id'), unique=True, nullable=False)
    company: Mapped["Company"] = relationship("Company", back_populates="manager", uselist=False)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

