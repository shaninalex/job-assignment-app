from passlib.hash import pbkdf2_sha256


def get_hashed_password(plain_text_password) -> str:
    return pbkdf2_sha256.hash(plain_text_password)


def check_password(plain_text_password, hashed_password):
    return pbkdf2_sha256.verify(plain_text_password, hashed_password)
