from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

from app.db import Role


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


class PositionSkill(BaseModel):
    position_id: int
    skill: int


class ApplyPayload(BaseModel):
    name: str
    email: str
    phone: str
    about: str
    position_id: int
    skills: Optional[List[Skill]]


class Candidate(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    about: str
    submitted: bool
    position: Optional[Position] = None
    created_at: str

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "about": self.about,
            "submitted": self.submitted,
            "position": self.position.to_json(),
            "created_at": str(self.created_at),
        }


class User(BaseModel):
    id: int
    email: str
    created_at: datetime
    role: Role

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.name,
            "created_at": str(self.created_at),
        }
