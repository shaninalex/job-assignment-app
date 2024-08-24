from sqlalchemy.orm import relationship


from .models import Base

# models
from .models.admin import Staff
from .models.candidate import Candidate, CandidateExperience
from .models.company import Company, CompanyManager
from .models.user import User, ConfirmCode
from globalTypes import AuthStatus, ConfirmStatusCode, CompanyManagerRole

User.candidate = relationship("Candidate", back_populates="user")


Base.registry.configure()
