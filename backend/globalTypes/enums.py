import enum


class RegistrationType(enum.Enum):
    COMPANY = "company"
    CANDIDATE = "candidate"


class Role(enum.Enum):
    CANDIDATE = "candidate"
    COMPANY_MANAGER = "company_manager"
    COMPANY_ADMIN = "company_admin"
