from typing import Tuple, Union
from sqlalchemy.orm import selectinload
from typing_extensions import Self
from pydantic import BaseModel, EmailStr, model_validator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import Role, AuthStatus, ConfirmStatusCode
from app.db.models.user import ConfirmCode, User
from app.utilites.generate_random_code import generate_numeric_code
from app.utilites.password import create_password_hash


async def get_user_by_id(session: AsyncSession, user_id: int) -> Union[User, None]:
    q = await session.execute(select(User).where(User.id == user_id).options(selectinload(User.codes)))
    return q.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> Union[User, None]:
    q = await session.execute(select(User).where(User.email == email).options(selectinload(User.codes)))
    return q.scalar_one_or_none()


class CreateUserPayload(BaseModel):
    name: str
    email: EmailStr
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.password_confirm
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self


async def create_candidate(session: AsyncSession, payload: CreateUserPayload) -> Tuple[User, ConfirmCode]:
    if await get_user_by_email(session, payload.email):
        raise ValueError("user already exist")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=create_password_hash(payload.password),
        role=Role.CANDIDATE,
        status=AuthStatus.PENDING,
        codes=[
            
        ]
    )
    confirm_code = ConfirmCode(
        user=user,
        code=generate_numeric_code(6),
        status=ConfirmStatusCode.CREATED,
    )
    session.add(user)
    session.add(confirm_code)
    await session.commit()
    await session.refresh(user)
    await session.refresh(confirm_code)
    return user, confirm_code



