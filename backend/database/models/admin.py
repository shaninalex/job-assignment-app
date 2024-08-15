from . import Base

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

ADMIN_PREFIX = "admin_"

class Staff(Base):
    __tablename__ = ADMIN_PREFIX + "staff"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100), unique=True)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }
