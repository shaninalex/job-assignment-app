"""
Module responsible for issuing, validating and refreshing app jwt tokens.

Docs:
  https://pyjwt.readthedocs.io/en/latest/usage.html
"""

from datetime import datetime, timedelta

import jwt

from app.db.models.user import User


def create_jwt_token(secret: str, user: User) -> str:
    """
    Generate user jwt token
    """
    expiration_time = datetime.now() + timedelta(days=1)
    exp_unix_timestamp = int(expiration_time.timestamp())
    iat_unix_timestamp = int(datetime.now().timestamp())
    claims = {
        "sub": str(user.id),
        "exp": exp_unix_timestamp,
        "iat": iat_unix_timestamp,
        "roles": [str(user.role.value)],
    }
    access_token = jwt.encode(claims, secret, algorithm="HS256")
    return access_token
