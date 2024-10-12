from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from loguru import logger
from fastapi import APIRouter, Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.dependencies.get_current_user import get_current_user
from app.api.dependencies.user import get_company_user
from app.api.serializers import APIResponse
from app.db.models.user import User
from app.db.session import get_db_session
from app.db.operations.company_op import get_company_members as op_company_members


router = APIRouter(
    tags=["Company"],
    prefix="/api/v1/company",
    # route_class=CompanyRouter,
)

auth_scheme = HTTPBearer()

@router.get("/members", )
async def get_company_members(
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user: User = Depends(get_company_user),
    session: AsyncSession = Depends(get_db_session)
):
    company_members = await op_company_members(session, user.member.company.id)
    return JSONResponse(content=APIResponse(
        data=[{
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "image": user.image,
            "social_accounts": user.social_accounts,
            "status": user.status,
            "role":user.role,
        } for user in company_members]

    ).model_dump()) 

