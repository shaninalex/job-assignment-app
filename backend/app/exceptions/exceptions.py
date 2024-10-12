class BaseApiError(Exception):
    """base exception class"""

    def __init__(self, message: str = "Service is unavailable", name: str = "API"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class ServiceError(BaseApiError):
    """failures in external services or APIs, like a database or a third-party service"""

    pass


class UserNotFoundError(ServiceError):
    pass


class ConfirmCodeNotFound(ServiceError):
    pass


class ConfirmCodeAlreadyUsed(ServiceError):
    pass
