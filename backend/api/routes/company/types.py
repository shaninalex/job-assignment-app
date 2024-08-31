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


class PositionFormPatch(BaseModel, extra="forbid"):
    title: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[str] = None
    requirements: Optional[str] = None
    interview_stages: Optional[str] = None
    offer: Optional[str] = None
    price_range: Optional[str] = None
    remote: Optional[Remote] = None
    salary: Optional[SalaryType] = None
    hours: Optional[WorkingHours] = None
    travel: Optional[TravelRequired] = None
    status: Optional[PositionStatus] = None
