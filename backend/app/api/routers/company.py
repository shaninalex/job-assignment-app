from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.user import get_user_if_role
from app.api.serializers import APIResponse, APIResponseGen
from app.api.serializers.user import APIPublicUser
from app.db.models.user import User
from app.db.operations.company_op import get_company_members as op_company_members
from app.db.session import get_db_session
from app.enums import Role

router = APIRouter(
    tags=["Company"],
    prefix="/api/v1/company",
)

auth_scheme = HTTPBearer()


@router.get("/members")
async def get_company_members_handler(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
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


@router.patch("/company")
async def get_company_handler(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER, Role.COMPANY_HR])),
    session: AsyncSession = Depends(get_db_session),
):
    return JSONResponse(content=APIResponse(data={}, status=True), status_code=status.HTTP_200_OK)


@router.patch("/company")
async def patch_company_handler(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN])),
    session: AsyncSession = Depends(get_db_session),
):
    return JSONResponse(content=APIResponse(data={}, status=True), status_code=status.HTTP_200_OK)


@router.patch("/company/disable")
async def disable_company_handler(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN])),
    session: AsyncSession = Depends(get_db_session),
):
    return JSONResponse(content=APIResponse(data={}, status=True), status_code=status.HTTP_200_OK)


@router.get("/positions")
async def list_positions_handler(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER, Role.COMPANY_HR])),
    session: AsyncSession = Depends(get_db_session),
):
    return JSONResponse(content=APIResponse(data={}, status=True), status_code=status.HTTP_201_CREATED)


@router.post("/position")
async def create_position_handler(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user: User = Depends(get_user_if_role([Role.COMPANY_ADMIN, Role.COMPANY_MEMBER])),
    session: AsyncSession = Depends(get_db_session),
):
    return JSONResponse(content=APIResponse(data={}, status=True), status_code=status.HTTP_201_CREATED)


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
