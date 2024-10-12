import uuid

from sqlalchemy import UUID, String, Text, ForeignKey, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import Base, Company
from app.db.models.utils import CreatedUpdatedFields
from app.enums import PositionStatus, Remote, SalaryType, TravelRequired, WorkingHours


class Position(Base, CreatedUpdatedFields):
    __tablename__ = "positions"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    responsibilities: Mapped[str] = mapped_column(Text)
    requirements: Mapped[str] = mapped_column(Text)
    interview_stages: Mapped[str] = mapped_column(Text)
    offer: Mapped[str] = mapped_column(Text)
    company_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("company.id"))
    remote: Mapped[Remote] = mapped_column(Enum(Remote))
    salary: Mapped[SalaryType] = mapped_column(Enum(SalaryType))
    hours: Mapped[WorkingHours] = mapped_column(Enum(WorkingHours))
    travel: Mapped[TravelRequired] = mapped_column(Enum(TravelRequired))
    status: Mapped[PositionStatus] = mapped_column(Enum(PositionStatus))
    price_range: Mapped[str] = mapped_column(String(100))

    company: Mapped["Company"] = relationship("Company", back_populates="positions")  # type: ignore # noqa
    # TODO: company member who created this ( or member who responsible for this)
