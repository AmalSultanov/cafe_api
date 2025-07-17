class AppException(Exception):
    pass


class ConflictError(AppException):
    pass


class NotFoundError(AppException):
    pass


class ValidationError(AppException):
    pass
