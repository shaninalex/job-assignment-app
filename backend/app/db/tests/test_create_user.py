import pytest
import uuid

from app.db.models import User
from app.db.operations import create_user
from app.enums import AuthStatus, ConfirmStatusCode, Role
from app.utilites.password import check_password


@pytest.mark.asyncio
async def test_create_user(session):
    async with session() as session:
        user = User(
            name="test",
            email="test@test.com",
            active=True,
            status=AuthStatus.ACTIVE,
            role=Role.CANDIDATE,
            password_hash="password_hash",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        assert user.id is not None
        assert user.id == 1


@pytest.mark.asyncio
async def test_create_candidate(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = create_user.CreateUserPayload(
            name=str(u),
            email=f"{str(u)}@test.com",
            password="testtest",
            password_confirm="testtest",
        )
        user, confirm_code = await create_user.create_candidate(session, payload)
        assert user is not None
        assert user.id is not None
        assert user.email == payload.email
        assert user.name == payload.name
        assert user.password_hash != payload.password
        assert check_password(payload.password, user.password_hash)
        assert user.role == Role.CANDIDATE
        assert user.status == AuthStatus.PENDING

        assert confirm_code is not None
        assert confirm_code.status == ConfirmStatusCode.CREATED

        new_user = await create_user.get_user_by_email(session, user.email)
        assert new_user is not None
        assert new_user.id == 1
        assert new_user.codes is not None
        assert len(new_user.codes) == 1
        assert new_user.codes[0].status == ConfirmStatusCode.CREATED
        assert new_user.codes[0].code == confirm_code.code

