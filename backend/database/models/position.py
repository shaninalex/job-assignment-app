from datetime import datetime
import uuid

from sqlalchemy import text, func, ForeignKey, Boolean
from sqlalchemy.types import UUID, VARCHAR, Text, Enum, String, JSON
from sqlalchemy.orm import relationship, mapped_column, Mapped

from globalTypes import (
    Remote,
    SalaryType,
    WorkingHours,
    TravelRequired,
    PositionStatus,
)
from . import Base


class Position(Base):
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
    remote: Mapped[Remote] = mapped_column(Enum(Remote))
    salary: Mapped[SalaryType] = mapped_column(Enum(SalaryType))
    hours: Mapped[WorkingHours] = mapped_column(Enum(WorkingHours))
    travel: Mapped[TravelRequired] = mapped_column(Enum(TravelRequired))
    status: Mapped[PositionStatus] = mapped_column(Enum(PositionStatus))

    # NOTE: column ideas
    # - search_tags
    # - featured/important

    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    def json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "responsibilities": self.responsibilities,
            "requirements": self.requirements,
            "interview_stages": self.interview_stages,
            "offer": self.offer,
            "remote": str(self.remote.value),
            "salary": str(self.salary.value),
            "hours": str(self.hours.value),
            "travel": str(self.travel.value),
            "status": str(self.status.value),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class PositionViews(Base):
    """PositionViews tracking.
    Since positions is public we views can by or not made by authorized account.
    That's why user_is nullable=True"""

    __tablename__ = "positions_views"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )

    position_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("positions.id"))
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)

    def json(self):
        return {
            "id": str(self.id),
            "position_id": str(self.position_id),
            "user_id": str(self.user_id),
            "created_at": str(self.created_at),
        }


class PositionFeedback(Base):
    __tablename__ = "positions_feedbacks"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    position_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("positions.id"))
    message: Mapped[Text] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now(), nullable=True)
    user = relationship("User", back_populates="feedbacks")

    def json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "position_id": str(self.position_id),
            "message": self.message,
            "created_at": str(self.created_at),
        }

