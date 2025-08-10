from src.core.logging import logger
from src.exceptions.cart import CartAlreadyExistsError, CartNotFoundError
from src.repositories.cart.interface import ICartRepository
from src.schemas.cart import CartRead, CartPatchUpdate


class CartService:
    def __init__(self, repository: ICartRepository) -> None:
        self.repository = repository

    async def create_cart(self, user_id: int) -> CartRead:
        logger.info(f"Cart service: Creating cart for user {user_id}")

        if await self.repository.get_by_user_id(user_id):
            logger.warning(
                f"Cart service: Cart already exists for user {user_id}"
            )
            raise CartAlreadyExistsError(user_id)

        cart = await self.repository.create(user_id)
        logger.info(
            f"Cart service: Cart was created for user {user_id} with ID: {cart.id}"
        )

        return CartRead.model_validate(cart)

    async def get_cart_by_user_id(self, user_id: int) -> CartRead:
        logger.debug(f"Cart service: Getting cart for user {user_id}")
        cart = await self.repository.get_by_user_id(user_id)

        if not cart:
            logger.warning(
                f"Cart service: Cart was not found for user {user_id}"
            )
            raise CartNotFoundError(user_id)

        logger.debug(f"Cart service: Found cart {cart.id} for user {user_id}")
        return CartRead.model_validate(cart)

    async def update_cart(
        self, user_id: int, cart_data: CartPatchUpdate
    ) -> CartRead:
        logger.debug(f"Cart service: Updating cart for user {user_id}")
        cart = await self.repository.get_by_user_id(user_id)

        if not cart:
            logger.warning(
                f"Cart service: Cart not found for user {user_id} during update"
            )
            raise CartNotFoundError(user_id)

        upd_cart = await self.repository.update(
            user_id, cart_data.model_dump(exclude_unset=True)
        )
        logger.info(
            f"Cart service: Cart was updated successfully for user {user_id}"
        )

        return CartRead.model_validate(upd_cart)

    async def delete_cart_by_user_id(self, user_id: int) -> None:
        logger.debug(f"Cart service: Deleting cart for user {user_id}")
        cart = await self.repository.get_by_user_id(user_id)

        if not cart:
            logger.warning(
                f"Cart service: Cart was not found for "
                f"user {user_id} during deletion"
            )
            raise CartNotFoundError(user_id)

        await self.repository.delete(user_id)
        logger.info(f"Cart service: Cart deleted successfully for user {user_id}")
