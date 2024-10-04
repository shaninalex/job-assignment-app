from pkg.database import Base

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

Base.registry.configure()
