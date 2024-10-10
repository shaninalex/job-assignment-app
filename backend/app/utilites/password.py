import bcrypt


def create_password_hash(raw_password: str) -> str:
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
    return hash.decode("utf-8")


def check_password(test_password: str, hash: str) -> bool:
    return bcrypt.checkpw(test_password.encode("utf-8"), hash.encode("utf-8"))

