from dataclasses import dataclass


@dataclass
class JWTTOkenPayload:
    email: str
    exp: str
    sub: str
    active: bool
    iss: str


@dataclass
class JWTTOkenResponse:
    token: str
    refresh: str


@dataclass
class Position:
    id: int
    name: str
    description: str


@dataclass
class Candidate:
    id: int
    name: str
    email: str
    phone: str
    about: str
    submitted: bool
    position_id: Position
    created_at: str