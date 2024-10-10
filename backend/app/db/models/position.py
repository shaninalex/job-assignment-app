from datetime import datetime
from sqlalchemy import String, Text, func, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models import Base, Company
from app.enums import PositionStatus, Remote, SalaryType, TravelRequired, WorkingHours


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    responsibilities: Mapped[str] = mapped_column(Text)
    requirements: Mapped[str] = mapped_column(Text)
    interview_stages: Mapped[str] = mapped_column(Text)
    offer: Mapped[str] = mapped_column(Text)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"))

    remote: Mapped[Remote] = mapped_column(Enum(Remote))
    salary: Mapped[SalaryType] = mapped_column(Enum(SalaryType))
    hours: Mapped[WorkingHours] = mapped_column(Enum(WorkingHours))
    travel: Mapped[TravelRequired] = mapped_column(Enum(TravelRequired))
    status: Mapped[PositionStatus] = mapped_column(Enum(PositionStatus))
    price_range: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    company: Mapped["Company"] = relationship( # type: ignore # noqa
        "Company", 
        back_populates="positions"
    )

