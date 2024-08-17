import uuid
from . import Base

from sqlalchemy import UUID, String, text
from sqlalchemy.orm import mapped_column, Mapped


class Staff(Base):
    __tablename__ = "admin_staff"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email
        }