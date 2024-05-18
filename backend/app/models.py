from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class LoginPayload(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)


class AdminCreateUserPayload(LoginPayload):
    pass


class JWTTokenResponse(BaseModel):
    token: str


class Skill(BaseModel):
    id: Optional[int] = None
    name: str


class Position(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    skills: Optional[List[Skill]] = []

    def to_json(self):
        print(self.skills)
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "skills": [d.model_dump() for d in self.skills],
        }


class ApplyPayload(BaseModel):
    name: str
    email: str
    phone: str
    about: str
    position_id: int
    skills: Optional[List[Skill]]


class CandidateSubmissionPayload(BaseModel):
    submitted: bool
    reason: str
