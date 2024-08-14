from . import Base

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }
