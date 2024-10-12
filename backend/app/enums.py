from enum import StrEnum


class Role(StrEnum):
    CANDIDATE = "candidate"
    COMPANY_MEMBER = "company_member"
    COMPANY_ADMIN = "company_admin"
    COMPANY_HR = "company_hr"


class AuthStatus(StrEnum):
    ACTIVE = "active"  # healthy user
    INACTIVE = "inactive"  # not active
    BANNED = "banned"  # banned, not active
    PENDING = "pending"  # just created, waiting for registration confirm


# ConfirmationStatusCode have 3 states:
# created - when code was created but not sent via transport ( email/phone )
# sent - sent via transport
# used - code was used and ready to remove
class ConfirmStatusCode(StrEnum):
    CREATED = "created"
    SENT = "sent"
    USED = "used"


# Position related enums
class Remote(StrEnum):
    REMOTE = "remote"
    OFFICE = "office"
    PARTIAL = "partial"


class SalaryType(StrEnum):
    EXPERIENCE = "experience"
    STATIC = "static"
    HOURLY = "hourly"
    AGREEMENT = "agreement"


class WorkingHours(StrEnum):
    FULL_TIME = "full_time"
    PARTIAL = "partial"


class TravelRequired(StrEnum):
    REQUIRED = "required"
    NO_MATTER = "no_matter"
    HELP = "help"


class PositionStatus(StrEnum):
    ACTIVE = "active"
    HIDDEN = "hidden"
    CLOSED = "closed"
    REMOVED = "removed"  # position moved to "trash can"


class CompanyStatus(StrEnum):
    ACTIVE = "active"  # healthy company
    INACTIVE = "inactive"  # not active
    BANNED = "banned"  # banned, not active
    PENDING = "pending"  # just created, waiting for confirmation


class CompanyMemberStatus(StrEnum):
    ACTIVE = "active"  # healthy member
    PENDING = "pending"  # company waiting for user confirm invitation
