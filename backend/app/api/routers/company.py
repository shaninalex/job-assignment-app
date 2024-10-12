from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.user import get_user_if_role
from app.api.serializers import APIResponse, APIResponseGen
from app.api.serializers.user import APIPublicUser
from app.db.models.user import User
from app.db.operations.company_op import (
    get_company_members as op_company_members,
    get_company_by_id,
    PartialCompanyPayload,
    patch_company,
    disable_company,
)
from app.db.operations.position_op import (
    positions_list,
    PartialPositionParamsPayload,
    position_create,
    PositionCreatePayload,
    position_get_by_id,
    position_update,
    PartialPositionUpdatePayload,
    position_delete,
)
from app.db.session import get_db_session
from app.enums import Role, CompanyStatus, PositionStatus, TravelRequired, WorkingHours, SalaryType, Remote

router = APIRouter(
    tags=["Company"],
    prefix="/api/v1/company",
)

auth_scheme = HTTPBearer()


@router.get("/members")
async def get_company_members_handler(
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponseGen[List[APIPublicUser]]:
    company_members = await op_company_members(session, user.member.company.id)
    return APIResponseGen(
        data=[
            APIPublicUser(
                id=user.id,
                name=user.name,
                email=user.email,
                image=user.image,
                social_accounts=user.social_accounts,
                status=user.status,
                role=user.role,
            )
            for user in company_members
        ]
    )


# TODO: company members crud


class APICompany(BaseModel):
    name: str
    website: str
    email: str
    status: CompanyStatus
    image_link: Optional[str] = None


@router.get("/company")
async def get_company_handler(
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER, Role.COMPANY_HR])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponseGen[APICompany]:
    company = await get_company_by_id(session, user.member.company_id)
    return APIResponseGen(
        data=APICompany(
            name=company.name,
            website=company.website,
            email=company.email,
            image_link=company.image_link,
            status=company.status,
        )
    )


@router.patch("/company")
async def patch_company_handler(
    payload: PartialCompanyPayload,
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponseGen[APICompany]:
    company = await patch_company(session, user.member.company_id, payload)
    return APIResponseGen(data=company)


@router.patch("/company/disable")
async def disable_company_handler(
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponse:
    await disable_company(session, user.member.company_id)
    return APIResponse(messages=["Company disabled"])


class APIPosition(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: str
    responsibilities: Optional[str] = None
    requirements: Optional[str] = None
    interview_stages: Optional[str] = None
    offer: Optional[str] = None
    company_id: Optional[UUID] = None
    remote: Optional[Remote] = None
    salary: Optional[SalaryType] = None
    hours: Optional[WorkingHours] = None
    travel: Optional[TravelRequired] = None
    status: Optional[PositionStatus] = None
    price_range: Optional[str] = None


@router.get("/positions")
async def list_positions_handler(
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER, Role.COMPANY_HR])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponseGen[List[APIPosition]]:
    positions = await positions_list(session, PartialPositionParamsPayload(company_id=user.member.company_id))
    api_positions: List[APIPosition] = []
    for p in positions:
        api_positions.append(APIPosition(**p.__dict__))
    return APIResponseGen(data=api_positions)


@router.post("/position")
async def create_position_handler(
    payload: APIPosition,
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponseGen[APIPosition]:
    position_create_payload = PositionCreatePayload(
        **payload.model_dump(exclude_unset=True), company_id=user.member.company_id
    )
    position = await position_create(session, position_create_payload)
    payload.id = position.id
    payload.status = position.status
    return APIResponseGen(data=payload)


@router.get("/position/{position_id}")
async def get_position_handler(
    position_id: UUID,
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponseGen[APIPosition]:
    position = await position_get_by_id(session, position_id=position_id, company_id=user.member.company_id)
    return APIResponseGen(data=position)


@router.patch("/position/{position_id}")
async def update_position_handler(
    position_id: UUID,
    payload: PartialPositionUpdatePayload,
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponseGen[APIPosition]:
    position = await position_update(
        session, position_id=position_id, payload=payload, company_id=user.member.company_id
    )
    out = APIPosition(**position.__dict__)
    return APIResponseGen(data=out)


@router.delete("/position/{position_id}")
async def delete_position_handler(
    position_id: UUID,
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponse:
    await position_delete(session, position_id=position_id, company_id=user.member.company_id)
    return APIResponse(message=[f"Position {position_id} deleted"], status=True)
