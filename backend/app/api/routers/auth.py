from loguru import logger
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.api.serializers import APIResponse
from app.api.serializers.auth import APILoginPayload, APIRegisterCandidatePayload, APICreateCompanyPayload
from app.api.serializers.user import APIConfirmCodePayload, create_public_user_object
from app.config import settings
from app.db.operations.user_op import ConfirmCodePayload, UserPayload, confirm_user, create_user, get_user_by_email
from app.db.operations.company_op import create_company, CreateCompanyPayload
from app.db.session import get_db_session
from app.enums import Role
from app.utilites.jwt import create_jwt_token
from app.utilites.password import check_password


router = APIRouter(prefix="/api/v1/auth")


@router.post("/register")
async def register_candidate(payload: APIRegisterCandidatePayload, session: AsyncSession = Depends(get_db_session)):
    db_payload = UserPayload(**payload.model_dump())
    user, confirm_code = await create_user(session, db_payload, Role.CANDIDATE)
    logger.debug(f"AMQP: New user: {user.email}. confirm_code: {confirm_code.code}")
    return {
        "status": True,
    }


@router.post("/register/company")
async def register_company(payload: APICreateCompanyPayload, session: AsyncSession = Depends(get_db_session)):
    db_payload = CreateCompanyPayload(**payload.model_dump())
    company, user, confirm_code = await create_company(session, db_payload)
    logger.debug(f"AMQP: New company: {company.name}. User: {user.email}. confirm_code: {confirm_code.code}")
    return {"status": True}


@router.post("/login")
async def register_login(payload: APILoginPayload, session: AsyncSession = Depends(get_db_session)):
    user = await get_user_by_email(session, payload.email)
    if not check_password(payload.password, user.password_hash):
        return JSONResponse(
            content=APIResponse(message=["Invalid credentials"], status=False).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    token = create_jwt_token(settings.secret, user)
    return APIResponse(
        data={
            "token": token,
            "user": create_public_user_object(user),
        },
        message=["Login successfull"],
    )


# IDEA: different confirmation methods ( email, phone ) ?
@router.post("/confirm/{hash}", description="Simplified user confirmation.")
async def confirm_account(hash: str, payload: APIConfirmCodePayload, session: AsyncSession = Depends(get_db_session)):
    code = ConfirmCodePayload(code=payload.code, key=hash)
    await confirm_user(session, code)
    return APIResponse(
        data={
            "confirmed": True,
        },
        message=["User successfully confirmed"],
    )
