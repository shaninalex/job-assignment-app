from collections.abc import Callable
from functools import wraps
from typing import List, Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.db.operations.user_op import get_user_by_id
from app.db.session import get_db_session
from app.enums import Role
from app.utilites.jwt import get_jwt_claims
from app.config import settings
from app.db.models import User

auth_scheme = HTTPBearer()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    """Extract the user from the JWT token and fetch from DB."""
    try:
        claims = get_jwt_claims(settings.secret, token.credentials)
        user = await get_user_by_id(session, UUID(claims.sub))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

async def get_company_user(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    """Extract the user from the JWT token and fetch from DB."""
    # try:
    claims = get_jwt_claims(settings.secret, token.credentials)
    user = await get_user_by_id(session, UUID(claims.sub), active=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if user.role == Role.CANDIDATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permissions to get this resource",
        )
    return user
    # except Exception as e:
    #     logger.error(f"Authentication failed: {e}")
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid or expired token",
    #     )

# TODO: create configurable dependency for different set of Role's


