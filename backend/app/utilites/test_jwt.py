import uuid

from app.db.models import User
from app.enums import Role
from app.utilites.jwt import create_jwt_token, get_jwt_claims

TEST_SECRET = "test_secret_code"


def test_create_and_parse_jwt():
    user = User(
        id=uuid.uuid4(),
        role=Role.CANDIDATE,
    )

    token = create_jwt_token(TEST_SECRET, user)
    assert token is not None
    assert token != ""

    claims = get_jwt_claims(TEST_SECRET, token)
    assert claims.sub == str(user.id)
    assert claims.roles == [user.role]
