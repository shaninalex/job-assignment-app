from sqlalchemy.ext.asyncio import AsyncSession

from api.routes.public.typing import RegistrationPayload
from pkg import password, utils
from pkg.consts import Role, AuthStatus, ConfirmStatusCode
from pkg.models import User, ConfirmCode
from pkg.repositories.user_repository import UserRepository
from pkg.services.event_publisher import EventPublisher


class UserService:
    def __init__(self, repository: UserRepository, event_service: EventPublisher):
        self.repository = repository
        self.event_service = event_service

    async def create_user(self, session: AsyncSession, payload: RegistrationPayload, role: Role):
        user = await self.repository.get_user(session, email=payload.email)
        if user:
            raise Exception("User already exists")

        user = User(
            name=payload.name,
            email=payload.email,
            role=role,
            status=AuthStatus.PENDING,
            password_hash=password.get_hashed_password(payload.password),
            codes=[
                ConfirmCode(
                    code=utils.generate_code(6),
                    status=ConfirmStatusCode.CREATED,
                )
            ],
        )
        user = await self.repository.create(session, user)
        return user
