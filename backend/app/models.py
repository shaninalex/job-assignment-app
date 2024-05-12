from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class LoginPayload(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)


class AdminCreateUserPayload(LoginPayload):
    pass


class JWTTokenResponse(BaseModel):
    token: str


class Position(BaseModel):
    id: int
    name: str
    description: str


class Candidate(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    about: str
    submitted: bool
    position_id: Position
    created_at: str


class User(BaseModel):
    id: int
    email: str
    created_at: datetime

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": str(self.created_at)  # .strftime("%d-%m-%Y")
        }
