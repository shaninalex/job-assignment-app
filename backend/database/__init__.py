from sqlalchemy.orm import relationship, Mapped


from .models import Base

from globalTypes import (
    RegistrationType,
    Role,
    AuthStatus,
    ConfirmStatusCode,
    Remote,
    SalaryType,
    WorkingHours,
    TravelRequired,
    PositionStatus,
)

# models
from .models.admin import Staff
from .models.candidate import Candidate, CandidateExperience
from .models.company import Company, CompanyManager
from .models.user import User, ConfirmCode
from .models.position import Position, PositionViews, PositionFeedback

# TODO: use lazy='' relationship attribute and move fields to it's own classes.
User.candidate = relationship("Candidate", back_populates="user")
Candidate.user = relationship("User", back_populates="candidate")

User.manager = relationship("CompanyManager", back_populates="user")
CompanyManager.user = relationship("User", back_populates="manager")

# User.feedbacks = relationship("PositionFeedback", uselist=True, back_populates="user")
# PositionFeedback.user = relationship("User", back_populates="feedbacks")

Base.registry.configure()
