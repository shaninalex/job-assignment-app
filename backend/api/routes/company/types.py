from pydantic import BaseModel
from typing import Optional
from globalTypes import (
    Remote,
    SalaryType,
    WorkingHours,
    TravelRequired,
    PositionStatus,
)

class PositionForm(BaseModel, extra="forbid"):
    title: str
    description: str
    responsibilities: str
    requirements: str
    interview_stages: str
    offer: str
    price_range: str
    remote: Remote
    salary: SalaryType
    hours: WorkingHours
    travel: TravelRequired
    status: PositionStatus
    company_id: Optional[str] = None
