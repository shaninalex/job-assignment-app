from aiohttp import web


class ExceptionNotFound(web.HTTPNotFound):
    def __init__(self, message="Resource not found"):
        super().__init__(text=message)


class ExceptionInvalidConfirmCode(web.HTTPBadRequest):
    def __init__(self, message="Invalid confirmation code"):
        super().__init__(text=message)


class ExceptionEmailAlreadyUsed(web.HTTPConflict):
    def __init__(self, message="Email is already in use"):
        super().__init__(text=message)
