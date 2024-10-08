import enum


class Role(enum.Enum):
    CANDIDATE = "candidate"
    COMPANY_MEMBER = "company_member"
    COMPANY_ADMIN = "company_admin"


class AuthStatus(enum.Enum):
    ACTIVE = "active"  # healthy user
    BANNED = "banned"  # banned, not active
    PENDING = "pending"  # just created, waiting for registration confirm


# ConfirmationStatusCode have 3 states:
# created - when code was created but not sent via transport ( email/phone )
# sent - sent via transport
# used - code was used and ready to remove
class ConfirmStatusCode(enum.Enum):
    CREATED = "created"
    SENT = "sent"
    USED = "used"


# Position related enums
class Remote(enum.Enum):
    REMOTE = "remote"
    OFFICE = "office"
    PARTIAL = "partial"


class SalaryType(enum.Enum):
    EXPERIENCE = "experience"
    STATIC = "static"
    HOURLY = "hourly"
    AGREEMENT = "agreement"


class WorkingHours(enum.Enum):
    FULL_TIME = "full_time"
    PARTIAL = "partial"


class TravelRequired(enum.Enum):
    REQUIRED = "required"
    NO_MATTER = "no_matter"
    HELP = "help"


class PositionStatus(enum.Enum):
    ACTIVE = "active"
    HIDDEN = "hidden"
    CLOSED = "closed"
    REMOVED = "removed"  # position moved to "trash can"
