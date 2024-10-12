from app.utilites.password import create_password_hash, check_password


def test_password():
    hash = create_password_hash("passwd")

    assert hash is not None
    assert check_password("wrong_passwd", hash) is not True
    assert check_password("passwd", hash)
