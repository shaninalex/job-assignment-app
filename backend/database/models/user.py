"""
User and auth related tables
=========================
"""

import uuid
from sqlalchemy import text, func, ForeignKey, Boolean
from sqlalchemy.types import UUID, VARCHAR, Text, Enum, String, JSON
from sqlalchemy.orm import relationship
from typing import List

from .const import AuthStatus, ConfirmStatusCode
from globalTypes import Role
from . import Base
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped


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
    active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"))
    image: Mapped[str] = mapped_column(Text, nullable=True)
    social_accounts: Mapped[JSON] = mapped_column(JSON, nullable=True)
    confirmed: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )
    role: Mapped[Role] = mapped_column(Enum(Role))
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    # mapped relationships
    codes: Mapped[List["ConfirmCode"]] = relationship(back_populates="user")

    def json(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "status": self.status.name,
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
        Enum(ConfirmStatusCode), default=ConfirmStatusCode.SENDED
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now())
    expired_at: Mapped[datetime] = mapped_column(default=func.now())

    # relationships
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="codes")

    def json(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "code": self.code,
            "status": self.status,
            "created_at": str(self.created_at),
            "user_id": str(self.user_id),
            "auth": self.auth.json(),
        }
