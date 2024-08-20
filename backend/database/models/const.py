import enum


class AuthStatus(enum.Enum):
    ACTIVE = "active"
    BANNED = "banned"
    PENDING = "pending"


class ConfirmStatusCode(enum.Enum):
    SENDED = "sended"
    USED = "used"


class CompanyManagerRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"