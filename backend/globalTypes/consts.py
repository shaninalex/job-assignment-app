import enum


class RegistrationType(enum.Enum):
    COMPANY = "company"
    CANDIDATE = "candidate"


class Role(enum.Enum):
    CANDIDATE = "candidate"
    COMPANY_MANAGER = "company_manager"
    COMPANY_ADMIN = "company_admin"


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
