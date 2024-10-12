from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
    id: Optional[UUID]
    title: str
    description: str
    responsibilities: Optional[str]
    requirements: Optional[str]
    interview_stages: Optional[str]
    offer: Optional[str]
    company_id: Optional[UUID]
    remote: Optional[Remote]
    salary: Optional[SalaryType]
    hours: Optional[WorkingHours]
    travel: Optional[TravelRequired]
    status: Optional[PositionStatus]
    price_range: Optional[str]


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


# NOTE: validation not complete
@router.post("/position")
async def create_position_handler(
    payload: APIPosition,
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER])),
    session: AsyncSession = Depends(get_db_session),
) -> APIResponseGen[List[APIPosition]]:
    position_create_payload = PositionCreatePayload(  # **payload.model_dump())
        title=payload.title,
        company_id=user.member.company_id,
        description=payload.description,
        interview_stages=payload.interview_stages,
        responsibilities=payload.responsibilities,
        requirements=payload.requirements,
        offer=payload.offer,
        remote=payload.remote,
        salary=payload.salary,
        hours=payload.hours,
        travel=payload.travel,
        status=payload.status,
        price_range=payload.price_range,
    )
    position = await position_create(session, position_create_payload)
    payload.id = position.id
    payload.status = position.status
    return APIResponseGen(data=payload)


@router.get("/position/{position_id}")
async def get_position_handler(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER])),
    session: AsyncSession = Depends(get_db_session),
):
    return JSONResponse(content=APIResponse(data={}, status=True), status_code=status.HTTP_200_OK)


@router.patch("/position/{position_id}")
async def update_position_handler(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER])),
    session: AsyncSession = Depends(get_db_session),
):
    return JSONResponse(content=APIResponse(data={}, status=True), status_code=status.HTTP_200_OK)


@router.delete("/position/{position_id}")
async def delete_position_handler(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER])),
    session: AsyncSession = Depends(get_db_session),
):
    return JSONResponse(content=APIResponse(data={}, status=True), status_code=status.HTTP_200_OK)
