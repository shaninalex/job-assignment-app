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
    price_range: Mapped[str] = mapped_column(String(100), nullable=True)
    responsibilities: Mapped[str] = mapped_column(Text, default="")
    requirements: Mapped[str] = mapped_column(Text, default="")
    interview_stages: Mapped[str] = mapped_column(Text, default="")
    offer: Mapped[str] = mapped_column(Text, default="")
    remote: Mapped[Remote] = mapped_column(Enum(Remote), default=Remote.REMOTE)
    salary: Mapped[SalaryType] = mapped_column(Enum(SalaryType), default=SalaryType.EXPERIENCE)
    hours: Mapped[WorkingHours] = mapped_column(Enum(WorkingHours), default=WorkingHours.FULL_TIME)
    travel: Mapped[TravelRequired] = mapped_column(Enum(TravelRequired), default=TravelRequired.NO_MATTER)
    status: Mapped[PositionStatus] = mapped_column(Enum(PositionStatus), default=PositionStatus.HIDDEN)

    company_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("company.id"))
    company: Mapped["Company"] = relationship("Company", back_populates="positions")  # type: ignore # noqa
    # TODO: company member who created this ( or member who responsible for this)
