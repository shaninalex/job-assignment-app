from typing import Any, Dict, Union
from pydantic import BaseModel
from app.db.models.user import User
from app.enums import AuthStatus, Role


class APIPublicUser(BaseModel):
    name: str
    email: str
    image: Union[str, None] = None
    social_accounts: Any
    status: AuthStatus
    role: Role


def create_public_user_object(user: User) -> APIPublicUser:
    return APIPublicUser(
        name=user.name,
        email=user.email,
        image=user.image,
        social_accounts=user.social_accounts,
        status=user.status,
        role=user.role,
    )


class APIPublicUserMe(BaseModel):
    name: str
    email: str
    settings: Dict
    image: str
    social_accounts: Dict
    confirmed: bool
    status: AuthStatus
    role: Role


class APIConfirmCodePayload(BaseModel, extra="forbid"):
    code: str
