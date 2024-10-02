from pkg.database.models import Base

# models
from .models import (
    Staff,
    Candidate,
    CandidateExperience,
    Company,
    CompanyManager,
    User,
    ConfirmCode,
    Position,
    PositionViews,
    PositionFeedback,
)


# User.feedbacks = relationship("PositionFeedback", uselist=True, back_populates="user")
# PositionFeedback.user = relationship("User", back_populates="feedbacks")

Base.registry.configure()
