# Module responsible for issuing, validating and refreshing app jwt tokens.
# Docs:
#   https://pyjwt.readthedocs.io/en/latest/usage.html

import jwt
from datetime import datetime, timedelta

from app.models import User, JWTTokenResponse
from app.settings import JWT_SECRET


def create_jwt_token(user: User) -> JWTTokenResponse:
    """
    Generate user jwt token
    Parameters
    ----------
    user : User
        User object for jwt claims
    Returns
    -------
    list
        signed jwt access token packed in JWTTokenResponse type
    """
    expiration_time = datetime.now() + timedelta(days=1)
    exp_unix_timestamp = int(expiration_time.timestamp())
    iat_unix_timestamp = int(datetime.now().timestamp())
    claims = {
        "sub": user.id,
        "exp": exp_unix_timestamp,
        "iat": iat_unix_timestamp
    }

    access_token = jwt.encode(claims, JWT_SECRET, algorithm="HS256")
    return JWTTokenResponse(token=access_token)
