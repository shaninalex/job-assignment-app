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
