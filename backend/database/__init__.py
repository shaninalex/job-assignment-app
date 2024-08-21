from sqlalchemy.orm import relationship


from .models import Base

# models
from .models.admin import Staff
from .models.candidate import Candidate, CandidateExperience
from .models.company import Company, CompanyManager
from .models.auth import Auth, ConfirmCode
from .models.const import AuthStatus, ConfirmStatusCode, CompanyManagerRole


Candidate.auth = relationship("Auth", back_populates="candidate")
CompanyManager.auth = relationship("Auth", back_populates="company_manager")

Base.registry.configure()