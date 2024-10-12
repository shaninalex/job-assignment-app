"""
Module responsible for issuing, validating and refreshing app jwt tokens.

Docs:
  https://pyjwt.readthedocs.io/en/latest/usage.html
"""

from datetime import datetime, timedelta
from typing import List
from uuid import UUID

import jwt
from pydantic import BaseModel

from app.db.models.user import User
from app.enums import Role


class JWTClaims(BaseModel, extra="forbid"):
    sub: str
    exp: int
    iat: int
    roles: List[Role]


def create_jwt_token(secret: str, user: User) -> str:
    """
    Generate user jwt token
    """
    expiration_time = datetime.now() + timedelta(days=1)
    exp_unix_timestamp = int(expiration_time.timestamp())
    iat_unix_timestamp = int(datetime.now().timestamp())
    claims = JWTClaims(
        sub=str(user.id),
        exp=exp_unix_timestamp,
        iat=iat_unix_timestamp,
        roles=[user.role],
    )
    access_token = jwt.encode(claims.model_dump(), secret, algorithm="HS256")
    return access_token


def get_jwt_claims(secret: str, token: str) -> JWTClaims:
    raw_claims = jwt.decode(token, secret, algorithms=["HS256"])
    claims = JWTClaims(**raw_claims)
    return claims


