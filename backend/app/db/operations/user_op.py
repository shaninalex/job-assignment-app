from typing import Tuple
from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing_extensions import Self

from app.db.models.user import ConfirmCode, User
from app.db.operations.confirm_code_op import get_confirm_code
from app.enums import Role, AuthStatus, ConfirmStatusCode
from app.exceptions.exceptions import ConfirmCodeAlreadyUsed, UserNotFoundError
from app.utilites.generate_random_code import generate_numeric_code, generate_string_code
from app.utilites.password import is_password_valid, create_password_hash


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User:
    q = await session.execute(select(User).where(User.id == user_id).options(selectinload(User.codes)))
    user = q.scalar_one_or_none()
    if user is None:
        raise UserNotFoundError(f"User with ID {str(user_id)} not found.")
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    q = await session.execute(select(User).where(User.email == email).options(selectinload(User.codes)))
    user = q.scalar_one_or_none()
    if user is None:
        raise UserNotFoundError(f"User with email {email} not found.")
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
        user=user, code=generate_numeric_code(6), status=ConfirmStatusCode.CREATED, key=generate_string_code(128)
    )
    session.add(user)
    session.add(confirm_code)
    await session.flush()
    return user, confirm_code


class ConfirmCodePayload(BaseModel, extra="forbid"):
    code: str
    key: str


async def confirm_user(session: AsyncSession, code: ConfirmCodePayload):
    confirm_code = await get_confirm_code(session, key=code.key, code=code.code)
    # we do not need to check is confirm_code is SENT since in this case user cannot know the confirm code
    # key and code since code was not sent.
    if confirm_code.status == ConfirmStatusCode.USED:
        raise ConfirmCodeAlreadyUsed(message="Confirm code is already used.")

    user = await get_user_by_id(session, confirm_code.user.id)
    user.status = AuthStatus.ACTIVE
    user.confirmed = True
    confirm_code.status = ConfirmStatusCode.USED
    await session.flush()
