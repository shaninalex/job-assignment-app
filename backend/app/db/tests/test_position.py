import uuid

import pytest

from app.core.core_types import Pagination
from app.db.operations.company_op import CreateCompanyOnlyPayload, create_company_only
from app.db.operations.position_op import (
    PartialPositionParamsPayload,
    PartialPositionUpdatePayload,
    PositionNotFoundError,
    position_create,
    PositionCreatePayload,
    position_delete,
    position_get_by_id,
    position_update,
    positions_list,
)
from app.enums import Remote, SalaryType, WorkingHours, TravelRequired, PositionStatus


@pytest.mark.asyncio
async def test_position_create(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyOnlyPayload(name=str(u), email=f"{str(u)}@test.com", website=f"https://{str(u)}.com")
        company = await create_company_only(session, payload)

        payload = PositionCreatePayload(
            title="position",
            company_id=company.id,
            description="description",
            interview_stages="interview_stages",
            responsibilities="responsibilities",
            requirements="requirements",
            offer="offer",
            price_range="price_range",
            remote=Remote.REMOTE,
            salary=SalaryType.EXPERIENCE,
            hours=WorkingHours.PARTIAL,
            travel=TravelRequired.NO_MATTER,
            status=PositionStatus.ACTIVE,
        )
        position = await position_create(session, payload)

        assert position.id is not None
        assert position.title == payload.title
        assert position.company_id == payload.company_id
        assert position.description == payload.description
        assert position.interview_stages == payload.interview_stages
        assert position.responsibilities == payload.responsibilities
        assert position.requirements == payload.requirements
        assert position.offer == payload.offer
        assert position.price_range == payload.price_range
        assert position.remote == payload.remote
        assert position.salary == payload.salary
        assert position.hours == payload.hours
        assert position.travel == payload.travel
        assert position.status == payload.status


@pytest.mark.asyncio
async def test_position_get_by_id(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyOnlyPayload(name=str(u), email=f"{str(u)}@test.com", website=f"https://{str(u)}.com")
        company = await create_company_only(session, payload)
        payload = PositionCreatePayload(
            title="position",
            company_id=company.id,
            description="description",
            interview_stages="interview_stages",
            responsibilities="responsibilities",
            requirements="requirements",
            offer="offer",
            price_range="price_range",
            remote=Remote.REMOTE,
            salary=SalaryType.EXPERIENCE,
            hours=WorkingHours.PARTIAL,
            travel=TravelRequired.NO_MATTER,
            status=PositionStatus.ACTIVE,
        )
        position = await position_create(session, payload)
        position_from_db = await position_get_by_id(session, position.id)
        assert position_from_db.title == payload.title
        assert position_from_db.company_id == payload.company_id
        assert position_from_db.description == payload.description


@pytest.mark.asyncio
async def test_position_update(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyOnlyPayload(name=str(u), email=f"{str(u)}@test.com", website=f"https://{str(u)}.com")
        company = await create_company_only(session, payload)
        payload = PositionCreatePayload(
            title="position",
            company_id=company.id,
            description="description",
            interview_stages="interview_stages",
            responsibilities="responsibilities",
            requirements="requirements",
            offer="offer",
            price_range="price_range",
            remote=Remote.REMOTE,
            salary=SalaryType.EXPERIENCE,
            hours=WorkingHours.PARTIAL,
            travel=TravelRequired.NO_MATTER,
            status=PositionStatus.ACTIVE,
        )
        position = await position_create(session, payload)
        position_from_db = await position_get_by_id(session, position.id)
        update_payload = PartialPositionUpdatePayload(
            title="position 123",
            description="description 123",
            responsibilities="responsibilities 123",
        )
        updated_position = await position_update(session, position_from_db.id, update_payload)
        assert updated_position.title == position_from_db.title
        assert updated_position.company_id == position_from_db.company_id
        assert updated_position.description == position_from_db.description


@pytest.mark.asyncio
async def test_position_delete(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyOnlyPayload(name=str(u), email=f"{str(u)}@test.com", website=f"https://{str(u)}.com")
        company = await create_company_only(session, payload)
        payload = PositionCreatePayload(
            title="position",
            company_id=company.id,
            description="description",
            interview_stages="interview_stages",
            responsibilities="responsibilities",
            requirements="requirements",
            offer="offer",
            price_range="price_range",
            remote=Remote.REMOTE,
            salary=SalaryType.EXPERIENCE,
            hours=WorkingHours.PARTIAL,
            travel=TravelRequired.NO_MATTER,
            status=PositionStatus.ACTIVE,
        )
        position = await position_create(session, payload)
        await position_delete(session, position.id, company.id)

        with pytest.raises(PositionNotFoundError):
            await position_get_by_id(session, position.id)


@pytest.mark.asyncio
async def test_position_list(session):
    async with session() as session:
        u = uuid.uuid4()
        payload = CreateCompanyOnlyPayload(name=str(u), email=f"{str(u)}@test.com", website=f"https://{str(u)}.com")
        company = await create_company_only(session, payload)
        payload = PositionCreatePayload(
            title="position",
            company_id=company.id,
            description="description",
            interview_stages="interview_stages",
            responsibilities="responsibilities",
            requirements="requirements",
            offer="offer",
            price_range="price_range",
            remote=Remote.REMOTE,
            salary=SalaryType.EXPERIENCE,
            hours=WorkingHours.PARTIAL,
            travel=TravelRequired.NO_MATTER,
            status=PositionStatus.ACTIVE,
        )
        position = await position_create(session, payload)
        payload2 = PositionCreatePayload(
            title="position",
            company_id=company.id,
            description="description",
            interview_stages="interview_stages",
            responsibilities="responsibilities",
            requirements="requirements",
            offer="offer",
            price_range="price_range",
            remote=Remote.PARTIAL,
            salary=SalaryType.HOURLY,
            hours=WorkingHours.FULL_TIME,
            travel=TravelRequired.REQUIRED,
            status=PositionStatus.HIDDEN,
        )
        position2 = await position_create(session, payload2)
        params = PartialPositionParamsPayload(
            company_id=company.id,
            remote=Remote.REMOTE,
            salary=SalaryType.EXPERIENCE,
            hours=WorkingHours.PARTIAL,
            travel=TravelRequired.NO_MATTER,
            status=PositionStatus.ACTIVE,
        )
        positions_by_params = await positions_list(session, params)
        assert len(positions_by_params) == 1
        found_position = positions_by_params[0]
        assert position.title == found_position.title
        assert position.description == found_position.description
        assert position.interview_stages == found_position.interview_stages
        assert position.responsibilities == found_position.responsibilities
        assert position.requirements == found_position.requirements
        assert position.offer == found_position.offer
        assert position.price_range == found_position.price_range
        assert position.remote == found_position.remote
        assert position.salary == found_position.salary
        assert position.hours == found_position.hours
        assert position.travel == found_position.travel
        assert position.status == found_position.status

        params = PartialPositionParamsPayload(
            company_id=company.id,
            remote=Remote.PARTIAL,
            salary=SalaryType.HOURLY,
            hours=WorkingHours.FULL_TIME,
            travel=TravelRequired.REQUIRED,
            status=PositionStatus.HIDDEN,
        )
        pagination = Pagination(limit=1, offset=1)
        positions_by_params = await positions_list(session, params=params, pagination=pagination)
        assert len(positions_by_params) == 1
        assert position2.id == positions_by_params[0].id
