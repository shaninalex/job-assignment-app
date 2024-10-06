import pytest
from sqlalchemy import select

from api.main import api_factory
from pkg.consts import ConfirmStatusCode, PositionStatus, Remote, SalaryType, TravelRequired, WorkingHours
from pkg.models.models import ConfirmCode, Position


@pytest.mark.asyncio(loop_scope="function")
async def test_create_position(aiohttp_client, test_config, async_session, test_app, cleanup):
    payload = {
        "name": "testCompany",
        "email": "testCompany@gmail.com",
        "password": "123",
        "password_confirm": "123",
        "type": "company_admin",
        "company_name": "ABC",
    }
    client = await aiohttp_client(test_app)
    resp = await client.post("/api/auth/register", json=payload)
    data = await resp.json()
    user_data = data["data"]["user"]
    async with async_session as session:
        confirm_code_query = select(ConfirmCode).where(
            (ConfirmCode.user_id == user_data["id"]) & (ConfirmCode.status == ConfirmStatusCode.SENT)
        )
        result = await session.execute(confirm_code_query)
        confirm_code = result.scalars().first()
        resp = await client.post(
            "/api/auth/confirm",
            json={
                "id": str(confirm_code.id),
                "code": confirm_code.code,
            },
        )

    # login
    resp = await client.post(
        "/api/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )
    data = await resp.json()

    # create position
    payload = {
        "title": "Junior engineer",
        "description": "Work at office",
        "responsibilities": "Fixing bugs",
        "requirements": "Understand datastructures and algorithms",
        "interview_stages": "3 stages",
        "offer": "work at office",
        "price_range": "600$-800$",
        "remote": "remote",
        "salary": "experience",
        "hours": "full_time",
        "travel": "no_matter",
        "status": "active",
        "company_id": data["data"]["company"]["id"]
    }

    # create position
    resp = await client.post(
        "/api/company/position", json=payload, headers={"Authorization": f"Bearer {data["data"]["token"]}"}
    )
    data = await resp.json()

    assert resp.status == 200, f"Expected status 200, got {resp.status}"
    assert data["data"]["id"] != ""
    assert data["data"]["title"] == payload["title"]
    assert data["data"]["description"] == payload["description"]
    assert data["data"]["responsibilities"] == payload["responsibilities"]
    assert data["data"]["requirements"] == payload["requirements"]
    assert data["data"]["interview_stages"] == payload["interview_stages"]
    assert data["data"]["offer"] == payload["offer"]
    assert data["data"]["price_range"] == payload["price_range"]
    assert data["data"]["remote"] == payload["remote"]
    assert data["data"]["salary"] == payload["salary"]
    assert data["data"]["hours"] == payload["hours"]
    assert data["data"]["travel"] == payload["travel"]
    assert data["data"]["status"] == payload["status"]

    async with async_session as session:
        confirm_code_query = select(Position).where(Position.id == data["data"]["id"])
        result = await session.execute(confirm_code_query)
        position: Position = result.scalars().first()
        assert str(position.id) == data["data"]["id"]
        assert position.title == payload["title"]
        assert position.description == payload["description"]
        assert position.responsibilities == payload["responsibilities"]
        assert position.requirements == payload["requirements"]
        assert position.interview_stages == payload["interview_stages"]
        assert position.offer == payload["offer"]
        assert position.price_range == payload["price_range"]
        assert position.remote == Remote.REMOTE
        assert position.salary == SalaryType.EXPERIENCE
        assert position.hours == WorkingHours.FULL_TIME
        assert position.travel == TravelRequired.NO_MATTER
        assert position.status == PositionStatus.ACTIVE
        assert str(position.company_id) == payload["company_id"]
