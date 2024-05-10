from pydantic import BaseModel, EmailStr, Field


class LoginPayload(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)

        
class JWTTOkenPayload(BaseModel):
    email: str
    exp: str
    sub: str
    active: bool
    iss: str


class JWTTokenResponse(BaseModel):
    token: str
    refresh: str


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
    created_at: str