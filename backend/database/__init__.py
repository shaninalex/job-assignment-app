from sqlalchemy.orm import relationship, Mapped


from .models import Base

# models
from .models.admin import Staff
from .models.candidate import Candidate, CandidateExperience
from .models.company import Company, CompanyManager
from .models.user import User, ConfirmCode
from globalTypes import AuthStatus, ConfirmStatusCode, RegistrationType, Role

User.candidate = relationship("Candidate", back_populates="user")
Candidate.user: Mapped["User"] = relationship("User", back_populates="candidate")

User.manager = relationship("CompanyManager", back_populates="user")
CompanyManager.user: Mapped["User"] = relationship("User", back_populates="manager")


Base.registry.configure()
