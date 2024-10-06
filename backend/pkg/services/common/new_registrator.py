from abc import ABC, abstractmethod
from os import name
from typing import Optional, Type, TypeVar, Generic, Union
import uuid

from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from pkg import password, utils
from pkg.consts import AuthStatus, ConfirmStatusCode, Role
from pkg.models.models import Company, CompanyManager, ConfirmCode, User
from pkg.services.event_service import Exchanges, IPublisher, RoutingKeys


# Define TypeVar for BaseModel subclasses
T = TypeVar("T", bound=BaseModel)


# Pydantic Models for Registration Data
class CandidateRegistration(BaseModel, extra="forbid"):
    name: str
    email: EmailStr
    password: str
    password_confirm: str


class CompanyRegistration(BaseModel, extra="forbid"):
    name: str
    email: EmailStr
    password: str
    password_confirm: str
    company_name: str
    company_email: str
    company_website: Optional[str] = None


class MemberRegistration(BaseModel, extra="forbid"):
    company_id: str
    registrator_user_id: str # id of a user who add this member
    name: str
    email: EmailStr
    password: str
    password_confirm: str


# Common Validators
class RegistrationValidator(ABC, Generic[T]):
    """Strategy for validation."""

    @abstractmethod
    def validate(self, payload: T):
        """Define validation logic."""
        pass


class CandidateValidator(RegistrationValidator[CandidateRegistration]):
    """Validation logic for a new candidate registration."""

    def validate(self, payload: CandidateRegistration):
        if payload.password != payload.password_confirm:
            raise ValueError("Passwords do not match")
        # session: AsyncSession,
        # Logic to check if user with this email exists
        # e.g., raise ValueError("User with this email already exists")
        pass


class CompanyValidator(RegistrationValidator[CompanyRegistration]):
    """Validation logic for a new user and company registration."""

    def validate(self, payload: CompanyRegistration):
        if payload.password != payload.password_confirm:
            raise ValueError("Passwords do not match")
        # session: AsyncSession,
        # Logic to check if user with this email exists
        # Logic to check if company with this name exists
        pass


class MemberValidator(RegistrationValidator[MemberRegistration]):
    """Validation logic for adding a new company member."""

    def validate(self, payload: MemberRegistration):
        if payload.password != payload.password_confirm:
            raise ValueError("Passwords do not match")
        # session: AsyncSession,
        # Logic to check if user with this email exists
        pass

# Factory Method for Registrator
class Registrator(Generic[T]):
    """Handle registration of new candidate, user + company, or add user to company."""

    def __init__(self, role: Role, publisher: IPublisher):
        self._validator: Optional[RegistrationValidator[T]] = None
        self._role = role
        self._publisher = publisher

    def set_validator(self, validator: RegistrationValidator[T]):
        """Set the specific validation strategy."""
        self._validator = validator

    def _create_user(self, payload: T) -> User:
        return User(
            id=uuid.uuid4(),
            email=payload.email,
            name=payload.name, 
            role=self._role,
            status=AuthStatus.PENDING,
            password_hash=password.get_hashed_password(payload.password),
            codes=[
                ConfirmCode(
                    code=utils.generate_code(6),
                    # The status should be:
                    # status=ConfirmStatusCode.CREATED
                    # But since we do not implement email service yet
                    # we will assume that confirm status is already sent
                    status=ConfirmStatusCode.SENT,
                )
            ],
        ) 

    async def register(self, payload: T, session: AsyncSession) -> Union[User, None]:
        """Process the registration using the appropriate validator."""
        if self._validator:
            errors = self._validator.validate(payload)
            if errors:
                raise ValueError(errors)

            # Logic for actual registration process
            try:
                await session.commit()
                user = self._create_user(payload)
                session.add(user)

                if self._role == Role.COMPANY_MEMBER:
                    session.add(CompanyManager(user=user, company_id=payload.company_id))
                if self._role == Role.COMPANY_ADMIN:
                    session.add(
                        Company(
                            name=payload.company_name,
                            email=payload.company_email,
                            website=payload.company_website,
                        )
                    )
            except Exception as e:
                # rollback if something went wrong
                await session.rollback()
                raise e

            # send rabbitMQ events
            await self._publisher.publish_event(Exchanges.ADMIN, RoutingKeys.NEW_USER, user.json())
            await self._publisher.publish_event(Exchanges.EMAIL, RoutingKeys.NEW_USER, user.json())
            return user
        else:
            raise ValueError("No validation strategy set")

    @staticmethod
    def create_registration(type_: Role) -> Type[T]:
        """Factory method to create registration payloads."""
        if type_ == Role.CANDIDATE:
            return CandidateRegistration
        elif type_ == Role.COMPANY_ADMIN:
            return CompanyRegistration
        elif type_ == Role.COMPANY_MEMBER:
            return MemberRegistration
        else:
            raise ValueError(f"Unknown registration type: {type_}")


async def registration_process(session: AsyncSession, type_: Role, data: dict, publisher: IPublisher) -> Union[User, None]:
    registration_class = Registrator.create_registration(type_)
    payload = registration_class(**data)
    registrator: Registrator = Registrator(type_, publisher)

    if type_ == Role.CANDIDATE:
        registrator.set_validator(CandidateValidator())
    elif type_ == Role.COMPANY_ADMIN:
        registrator.set_validator(CompanyValidator())
    elif type_ == Role.COMPANY_MEMBER:
        registrator.set_validator(MemberValidator())

    return await registrator.register(payload, session)



