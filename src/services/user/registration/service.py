from src.exceptions.cart import CartAlreadyExistsError
from src.exceptions.user import (
    UserAlreadyExistsError, UserIdentityAlreadyExistsError
)
from src.schemas.user import UserRegister, UserRead
from src.services.cart.interface import ICartService
from src.services.user.interface import IUserService


class UserRegistrationService:
    def __init__(
        self,
        user_service: IUserService,
        cart_service: ICartService
    ) -> None:
        self.user_service = user_service
        self.cart_service = cart_service

    async def register_user(self, user_data: UserRegister) -> UserRead:
        try:
            user = await self.user_service.create_user(user_data)
            user_cart = await self.cart_service.create_cart(user.id)
            return UserRead.model_validate(user)
        except UserAlreadyExistsError:
            raise
        except UserIdentityAlreadyExistsError:
            raise
        except CartAlreadyExistsError:
            raise
