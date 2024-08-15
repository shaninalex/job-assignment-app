import enum

class AuthStatus(enum.Enum):
    ACTIVE = 'active'
    BANNED = 'banned'
    PENDING = 'pending'
