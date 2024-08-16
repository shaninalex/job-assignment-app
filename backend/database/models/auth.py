import uuid
from sqlalchemy import text
from sqlalchemy.types import UUID, VARCHAR, Text, Enum
from .const import AuthStatus
from . import Base
from .candidate import Candidate
from .company import CompanyManager

from sqlalchemy.orm import mapped_column, Mapped, relationship


class Auth(Base):
    __tablename__ = "auth"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=text("uuid_generate_v4()"))
    hash: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(VARCHAR(100), unique=True)
    status: Mapped[AuthStatus] = mapped_column(Enum(AuthStatus))

    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="auth", uselist=False, cascade="all")
    company_manager: Mapped["CompanyManager"] = relationship("CompanyManager", back_populates="auth", uselist=False, cascade="all")

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "status": self.status,
        }


Candidate.auth = relationship("Auth", back_populates="candidate", uselist=False)
CompanyManager.auth = relationship("Auth", back_populates="company_manager", uselist=False, cascade="all")
