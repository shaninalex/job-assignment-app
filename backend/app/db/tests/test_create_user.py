import pytest

from app.db.models import User
from app.enums import AuthStatus, Role


@pytest.mark.asyncio
async def test_create_user(session):
    async with session() as session:
        user = User(
            name="test",
            email="test@test.com",
            active=True,
            status=AuthStatus.ACTIVE,
            role=Role.CANDIDATE,
            password_hash="sdkfhkasjdf",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        assert user.id is not None
        assert user.id == 1
