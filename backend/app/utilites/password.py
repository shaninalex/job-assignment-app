import bcrypt


def create_password_hash(raw_password: str) -> str:
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
    return hash.decode("utf-8")


def check_password(test_password: str, hash: str) -> bool:
    return bcrypt.checkpw(test_password.encode("utf-8"), hash.encode("utf-8"))


def is_password_valid(password: str | None, password_confirm: str | None) -> bool:
    # TODO: Add password strength check
    # doc: https://pypi.org/project/zxcvbn/
    # doc: https://pypi.org/project/password-strength/
    return password is not None and password_confirm is not None and password == password_confirm


# handmade password strength
# def password_strength(password):
#     if len(password) < 8:
#         return "Weak Password: Password must be at least 8 characters long."
#     if not re.search("[A-Z]", password):
#         return "Weak Password: Add at least one uppercase letter."
#     if not re.search("[a-z]", password):
#         return "Weak Password: Add at least one lowercase letter."
#     if not re.search("[0-9]", password):
#         return "Weak Password: Add at least one number."
#     if not re.search("[@#$%^&*]", password):
#         return "Weak Password: Include at least one special character."
#     return "Strong Password!"
