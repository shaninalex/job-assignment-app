import uuid

import pytest
from pydantic import ValidationError

from app.db.operations.user import UserPayload, create_user, get_user_by_email
from app.enums import AuthStatus, ConfirmStatusCode, Role
from app.utilites.password import check_password


@pytest.mark.asyncio
async def test_create_candidate(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = UserPayload(
            name=str(u),
            email=f"{str(u)}@test.com",
            password="testtest",
            password_confirm="testtest",
        )
        user, confirm_code = await create_user(session, payload, Role.CANDIDATE)
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

        new_user = await get_user_by_email(session, user.email)
        assert new_user is not None
        assert new_user.codes is not None
        assert len(new_user.codes) == 1
        assert new_user.codes[0].status == ConfirmStatusCode.CREATED
        assert new_user.codes[0].code == confirm_code.code


@pytest.mark.asyncio
async def test_invalid_payload():
    with pytest.raises(ValidationError) as exc_info:
        UserPayload(name="name", email="invalid-email", password="testtest_", password_confirm="testtest_")

    assert "value is not a valid email address" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        UserPayload(name="name", email="test@test.com", password="testtest_", password_confirm="different_password")

    assert "passwords do not match" in str(exc_info.value)
