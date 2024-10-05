# Module responsible for issuing, validating and refreshing app jwt tokens.
# Docs:
#   https://pyjwt.readthedocs.io/en/latest/usage.html

from datetime import datetime, timedelta

import jwt

from pkg.models import User
from pkg.settings import JWT_SECRET


def create_jwt_token(user: User) -> str:
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
        "sub": str(user.id),
        "exp": exp_unix_timestamp,
        "iat": iat_unix_timestamp,
        "roles": [str(user.role.value)],
    }
    access_token = jwt.encode(claims, JWT_SECRET, algorithm="HS256")
    return access_token
