from typing import Tuple

from pydantic import BaseModel, EmailStr, model_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing_extensions import Self

from app.db.models.user import ConfirmCode, User
from app.enums import Role, AuthStatus, ConfirmStatusCode
from app.utilites.generate_random_code import generate_numeric_code
from app.utilites.password import is_password_valid, create_password_hash


class UserNotFoundError(Exception):
    pass


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    q = await session.execute(select(User).where(User.id == user_id).options(selectinload(User.codes)))
    user = q.scalar_one_or_none()
    if user is None:
        raise UserNotFoundError(f"User with ID {user_id} not found.")
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    q = await session.execute(select(User).where(User.email == email).options(selectinload(User.codes)))
    user = q.scalar_one_or_none()
    if user is None:
        raise UserNotFoundError(f"User with email {user} not found.")
    return user


class UserPayload(BaseModel, extra="forbid"):
    name: str
    email: EmailStr
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if not is_password_valid(self.password, self.password_confirm):
            raise ValueError("passwords do not match")
        return self


async def create_user(session: AsyncSession, payload: UserPayload, role: Role) -> Tuple[User, ConfirmCode]:
    try:
        await get_user_by_email(session, payload.email)
    except UserNotFoundError:
        pass

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=create_password_hash(payload.password),
        role=role,
        status=AuthStatus.PENDING,
    )
    confirm_code = ConfirmCode(
        user=user,
        code=generate_numeric_code(6),
        status=ConfirmStatusCode.CREATED,
    )
    session.add(user)
    session.add(confirm_code)
    await session.flush()
    return user, confirm_code


class ConfirmCodePayload(BaseModel, extra="forbid"):
    code: str
    key: str


async def confirm_user(session: AsyncSession, code: ConfirmCodePayload, user_id: int):
    user = await get_user_by_id(session, user_id)

    # TODO: validate confirm code
    # IDEA: different confirmation methods ( email, phone ) ?

    user.status = AuthStatus.ACTIVE
    await session.flush()
    # await session.refresh(user)
