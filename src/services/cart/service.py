from src.exceptions.cart import CartAlreadyExistsError, CartNotFoundError
from src.repositories.cart.interface import ICartRepository
from src.schemas.cart import CartRead, CartPatchUpdate


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

    async def update_cart(
        self, user_id: int, cart_data: CartPatchUpdate
    ) -> CartRead:
        cart = await self.repository.get_by_user_id(user_id)

        if not cart:
            raise CartNotFoundError(user_id)

        upd_cart = self.repository.update(
            user_id, cart_data.model_dump(exclude_unset=True)
        )
        return CartRead.model_validate(upd_cart)

    async def delete_cart_by_user_id(self, user_id: int) -> None:
        cart = await self.repository.get_by_user_id(user_id)

        if not cart:
            raise CartNotFoundError(user_id)
        await self.repository.delete(user_id)
