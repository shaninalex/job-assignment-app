from .const import AuthStatus
from . import Base

from sqlalchemy import VARCHAR, Text, Enum
from sqlalchemy.orm import mapped_column, Mapped


class Auth(Base):
    __tablename__ = "auth"
    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(VARCHAR(100), unique=True)
    status: Mapped[AuthStatus] = mapped_column(Enum(AuthStatus))

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "status": self.status,
        }
