from src.exceptions.base import ConflictError, NotFoundError, ValidationError


class UserPhoneAlreadyExistsError(ConflictError):
    def __init__(self, phone_number: str):
        super().__init__(
            f"User with phone number +'{phone_number}' already exists"
        )


class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: int):
        super().__init__(f"User with ID={user_id} was not found")


class NoUserUpdateDataError(ValidationError):
    def __init__(self):
        super().__init__("No data provided for update")


class UserIdentityAlreadyExistsError(ConflictError):
    def __init__(self, username: str, provider: str):
        super().__init__(
            f"User with username '{username}' from {provider} already exists"
        )


class UserProviderIdAlreadyExistsError(ConflictError):
    def __init__(self, provider_id: str, provider: str):
        super().__init__(
            f"User with provider ID={provider_id} from {provider} already exists"
        )


class UserIdentityNotFoundError(NotFoundError):
    def __init__(self, provider_id: str, provider: str):
        super().__init__(
            f"User with provider ID={provider_id} from {provider} was not found"
        )


class UserPhoneError(ValidationError):
    def __init__(self):
        super().__init__("Phone number must contain only digits")
