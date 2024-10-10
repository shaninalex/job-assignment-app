from typing import List
from datetime import datetime
from sqlalchemy import Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models import Base
from app.enums import CompanyStatus


class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    website: Mapped[str] = mapped_column(String(100), unique=True) 
    email: Mapped[str] = mapped_column(String(100), unique=True) 
    image_link: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[CompanyStatus] = mapped_column(Enum(CompanyStatus))
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    positions: Mapped[List["Position"]] = relationship( # type: ignore # noqa
        "Position",
        back_populates="company",
        lazy="noload"  # or use lazy="joined" if you prefer eager loading
    )
