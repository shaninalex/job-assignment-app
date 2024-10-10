from datetime import datetime, timedelta
from typing import List

from sqlalchemy import String, Boolean, Text, JSON, VARCHAR, Enum, text, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from app.db.models import Base
from app.enums import AuthStatus, Role, ConfirmStatusCode


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
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
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=text("current_timestamp"), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=text("current_timestamp"),
        onupdate=func.now(),
        nullable=True,
    )

    codes: Mapped[List["ConfirmCode"]] = relationship("ConfirmCode", back_populates="user")


def default_expired_at():
    # Compute the default expiration time as `datetime.now() + 5 minutes`
    return datetime.now() + timedelta(minutes=5)


class ConfirmCode(Base):
    __tablename__ = "confirm_codes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
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
