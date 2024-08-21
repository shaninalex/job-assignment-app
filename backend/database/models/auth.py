import uuid
from typing import List
from sqlalchemy import text, func, ForeignKey
from sqlalchemy.types import UUID, VARCHAR, Text, Enum
from sqlalchemy.orm import relationship

from .const import AuthStatus, ConfirmStatusCode
from . import Base
from .candidate import Candidate 
from .company import CompanyManager
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped

# NOTE
# Mapping Class Inheritance Hierarchies¶
# https://docs.sqlalchemy.org/en/20/orm/inheritance.html
# Auth table can be applied to Candidate and CompanyMember. We need to decide is it worth it or not.


class Auth(Base):
    __tablename__ = "auth"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    hash: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(VARCHAR(100), unique=True)
    status: Mapped[AuthStatus] = mapped_column(Enum(AuthStatus))

    candidate: Mapped["Candidate"] = relationship(
        "Candidate", back_populates="auth", uselist=False)  # Set uselist=False for one-to-one relationship
    company_manager: Mapped["CompanyManager"] = relationship(
        "CompanyManager", back_populates="auth", uselist=False)
    codes: Mapped[List["ConfirmCode"]] = relationship(back_populates="auth")

    def json(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "status": self.status.name,
            "candidate": self.candidate.json() if self.candidate else None,
            "company_manager": self.company_manager.json() if self.company_manager else None,
            "codes": [code.json() for code in self.codes],
        }


class ConfirmCode(Base):
    __tablename__ = "confirm_codes"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    email: Mapped[str] = mapped_column(VARCHAR(100), unique=True)
    code: Mapped[str] = mapped_column(VARCHAR(6))
    status: Mapped[AuthStatus] = mapped_column(
        Enum(ConfirmStatusCode), default=ConfirmStatusCode.SENDED)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), nullable=True
    )
    auth_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("auth.id"))
    auth: Mapped["Auth"] = relationship(back_populates="codes")
    # TODO: expired date now+1 hour
    def json(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "code": self.code,
            "status": self.status,
            "created_at": str(self.created_at),
            "auth_id": str(self.auth_id),
            "auth": self.auth.json(),
        }
