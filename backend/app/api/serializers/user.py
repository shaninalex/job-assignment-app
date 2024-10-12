from typing import Any, Union
from uuid import UUID

from pydantic import BaseModel

from app.db.models.user import User
from app.enums import Role


class APIPublicUser(BaseModel):
    id: UUID
    name: str
    email: str
    image: Union[str, None] = None
    social_accounts: Any
    role: Role


def create_public_user_object(user: User) -> APIPublicUser:
    return APIPublicUser(
        id=user.id,
        name=user.name,
        email=user.email,
        image=user.image,
        social_accounts=user.social_accounts,
        role=user.role,
    )


class APIConfirmCodePayload(BaseModel, extra="forbid"):
    code: str
