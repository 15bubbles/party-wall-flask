class BaseException(Exception):
    def __init__(self, message: str, *args):
        self.message = message
        super().__init__(message, *args)


class DatabaseException(BaseException):
    pass


class RecordNotFound(DatabaseException):
    pass


class RecordAlreadyExists(DatabaseException):
    pass


class InvalidCredentials(BaseException):
    pass


class ValidationFailed(BaseException):
    pass
