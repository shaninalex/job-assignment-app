import uuid
from . import Base

from sqlalchemy import UUID, String, text
from sqlalchemy.orm import mapped_column, Mapped

ADMIN_PREFIX = "admin_"

class Staff(Base):
    __tablename__ = ADMIN_PREFIX + "staff"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("uuid_generate_v4()"))
    name: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100), unique=True)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }
