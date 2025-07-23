from src.exceptions.cart import CartAlreadyExistsError, CartNotFoundError
from src.repositories.cart.interface import ICartRepository
from src.schemas.cart import CartRead


class CartService:
    def __init__(self, repository: ICartRepository) -> None:
        self.repository = repository

    async def create_cart(self, user_id: int) -> CartRead:
        if await self.repository.get_by_user_id(user_id):
            raise CartAlreadyExistsError(user_id)

        cart = await self.repository.create(user_id)
        return CartRead.model_validate(cart)

    async def get_cart_by_user_id(self, user_id: int) -> CartRead:
        cart = await self.repository.get_by_user_id(user_id)

        if not cart:
            raise CartNotFoundError(user_id)
        return CartRead.model_validate(cart)

    async def delete_cart_by_user_id(self, user_id: int) -> None:
        cart = await self.repository.get_by_user_id(user_id)

        if not cart:
            raise CartNotFoundError(user_id)
        await self.repository.delete(user_id)
