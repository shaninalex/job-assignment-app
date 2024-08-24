import enum


class RegistrationType(enum.Enum):
    COMPANY = "company"
    CANDIDATE = "candidate"


class Role(enum.Enum):
    CANDIDATE = "candidate"
    COMPANY_MANAGER = "company_manager"
    COMPANY_ADMIN = "company_admin"


class AuthStatus(enum.Enum):
    ACTIVE = "active" # healthy user
    BANNED = "banned" # banned, not active
    PENDING = "pending" # just created, waiting for registration confirm


# ConfirmationStatusCode have 3 states:
# created - when code was created but not sended via transport ( email/phone )
# sended - sended via transport
# used - code was used and ready to remove
class ConfirmStatusCode(enum.Enum):
    CREATED = "created"
    SENDED = "sended"
    USED = "used"
