from src.core.logging import logger
from src.exceptions.cart import CartNotFoundError
from src.exceptions.cart_item import (
    CartItemNotFoundError, CartItemsNotFoundError, NoCartItemUpdateDataError
)
from src.message_broker.events.cart import CartUpdatedEvent
from src.message_broker.publisher.interface import IEventPublisher
from src.message_broker.topics import TOPIC_CART_UPDATED
from src.repositories.interfaces.cart_item import ICartItemRepository
from src.schemas.cart import CartPatchUpdate
from src.schemas.cart_item import (
    CartItemCreate, CartItemPatchUpdate, CartItemRead
)
from src.services.cart.interface import ICartService
from src.services.meal.interface import IMealService


class CartItemService:
    def __init__(
        self,
        repository: ICartItemRepository,
        cart_service: ICartService,
        meal_service: IMealService,
        publisher: IEventPublisher
    ) -> None:
        self.repository = repository
        self.cart_service = cart_service
        self.meal_service = meal_service
        self.publisher = publisher

    async def add_item_to_cart(
        self, user_id: int, item_data: CartItemCreate
    ) -> CartItemRead:
        logger.info(
            f"Cart item service: Adding item to cart for user {user_id}, "
            f"meal_id: {item_data.meal_id}"
        )

        try:
            cart = await self.cart_service.get_cart_by_user_id(user_id)
        except CartNotFoundError:
            logger.warning(
                f"Cart item service: Cart was not found for user {user_id}"
            )
            raise

        existing_item = await self.repository.get_by_cart_and_meal_id(
            cart.id, item_data.meal_id
        )
        if existing_item:
            logger.info(
                f"Cart item service: Item already exists in cart, "
                f"updating quantity from {existing_item.quantity} to "
                f"{existing_item.quantity + item_data.quantity}"
            )
            new_quantity = existing_item.quantity + item_data.quantity
            return await self.update_cart_item(
                user_id,
                existing_item.id,
                CartItemPatchUpdate(quantity=new_quantity)
            )

        meal = await self.meal_service.get_meal(item_data.meal_id)
        item_dict = item_data.model_dump()
        item_dict.update({
            "cart_id": cart.id,
            "unit_price": meal.unit_price,
            "meal_name": meal.name,
            "total_price": meal.unit_price * item_data.quantity,
        })

        logger.debug(f"Cart item service: Creating new cart item: {item_dict}")
        item = await self.repository.create(item_dict)

        new_cart_total = cart.total_price + item_dict["total_price"]
        logger.debug(
            f"Cart item service: Publishing cart update "
            f"event - new total: {new_cart_total}"
        )

        event = CartUpdatedEvent(
            user_id=user_id,
            cart_data=CartPatchUpdate(total_price=new_cart_total)
        )
        await self.publisher.publish(TOPIC_CART_UPDATED, event.model_dump())
        logger.info(
            f"Cart item was added for user {user_id}, item ID: {item.id}"
        )

        return CartItemRead.model_validate(item)

    async def get_cart_items(self, user_id: int) -> list[CartItemRead]:
        logger.debug(
            f"Cart item service: Getting cart items for user {user_id}"
        )
        cart = await self.cart_service.get_cart_by_user_id(user_id)

        if not cart:
            logger.warning(
                f"Cart item service: Cart was not found for user {user_id}"
            )
            raise CartNotFoundError(user_id)

        items = await self.repository.get_all_by_cart_id(cart.id)
        logger.debug(
            f"Cart item service: Retrieved {len(items)} cart items for user {user_id}"
        )

        return [CartItemRead.model_validate(item) for item in items]

    async def get_cart_item(self, user_id: int, item_id: int) -> CartItemRead:
        logger.debug(
            f"Cart item service: Getting cart item {item_id} for user {user_id}"
        )
        cart = await self.cart_service.get_cart_by_user_id(user_id)

        if not cart:
            logger.warning(
                f"Cart item service: Cart not found for user {user_id}"
            )
            raise CartNotFoundError(user_id)

        item = await self.repository.get_by_id(item_id)
        if item is None or item.cart_id != cart.id:
            logger.warning(
                f"Cart item service: Cart item {item_id} was not found "
                f"in user {user_id}'s cart"
            )
            raise CartItemNotFoundError(item_id)

        logger.debug(
            f"Cart item service: Found cart item {item_id}: {item.meal_name} "
            f"(qty: {item.quantity})"
        )
        return CartItemRead.model_validate(item)

    async def update_cart_item(
        self,
        user_id: int,
        item_id: int,
        item_data: CartItemPatchUpdate
    ) -> CartItemRead:
        logger.debug(
            f"Cart item service: Updating cart item {item_id} for user {user_id}"
        )
        new_data = item_data.model_dump(exclude_unset=True)

        if not new_data:
            logger.warning(
                f"Cart item service: No update data provided for cart item {item_id}"
            )
            raise NoCartItemUpdateDataError()

        cart = await self.cart_service.get_cart_by_user_id(user_id)
        if not cart:
            logger.warning(
                f"Cart item service: Cart was not found for user {user_id}"
            )
            raise CartNotFoundError(user_id)

        item = await self.repository.get_by_id(item_id)
        if not item or item.cart_id != cart.id:
            logger.warning(
                f"Cart item service: Cart item {item_id} was not found in "
                f"user {user_id}'s cart"
            )
            raise CartItemNotFoundError(item_id)

        if "quantity" in new_data:
            quantity = new_data["quantity"]
            if quantity == 0:
                logger.info(
                    f"Cart item service: Quantity set to 0, removing cart item {item_id}"
                )
                return await self.remove_item_from_cart(user_id, item_id)

            new_total_price = item.unit_price * quantity
            new_data["total_price"] = new_total_price
            new_cart_total = cart.total_price - item.total_price + new_total_price

            logger.debug(
                f"Cart item service:: Publishing cart update "
                f"event - new total: {new_cart_total}"
            )
            event = CartUpdatedEvent(
                user_id=user_id,
                cart_data=CartPatchUpdate(total_price=new_cart_total)
            )

            await self.publisher.publish(TOPIC_CART_UPDATED, event.model_dump())

        upd_item = await self.repository.update(item_id, new_data)
        logger.info(
            f"Cart item service: Cart item {item_id} "
            f"was updated successfully for user {user_id}"
        )
        return CartItemRead.model_validate(upd_item)

    async def remove_item_from_cart(self, user_id: int, item_id: int) -> None:
        logger.debug(
            f"Cart item service: Deleting cart item {item_id} for user {user_id}"
        )
        cart = await self.cart_service.get_cart_by_user_id(user_id)

        if not cart:
            logger.warning(
                f"Cart item service: Cart was not found for user {user_id}"
            )
            raise CartNotFoundError(user_id)

        item = await self.repository.get_by_cart_and_item_id(
            cart.id, item_id
        )
        if not item:
            logger.warning(
                f"Cart item service: Cart item was not found for user {user_id}"
            )
            raise CartItemNotFoundError(item_id)

        event = CartUpdatedEvent(
            user_id=user_id,
            cart_data=CartPatchUpdate(
                total_price=cart.total_price - item.total_price
            )
        )

        await self.publisher.publish(TOPIC_CART_UPDATED, event.model_dump())
        logger.info(
            f"Cart item service: CartUpdatedEvent was published for user "
            f"{user_id}'s cart"
        )
        logger.info(
            f"Cart item service: Deleting cart item {item.id} for user {user_id}"
        )
        await self.repository.delete_by_id(item.id)

    async def remove_items_from_cart(self, user_id: int) -> None:
        logger.debug(
            f"Cart item service: Deleting cart items for user {user_id}"
        )
        cart = await self.cart_service.get_cart_by_user_id(user_id)

        if not cart:
            logger.warning(
                f"Cart item service: Cart was not found for user {user_id}"
            )
            raise CartNotFoundError(user_id)

        items = await self.repository.get_all_by_cart_id(cart.id)
        if not items:
            logger.warning(
                f"Cart item service: Cart items were not found for user {user_id}"
            )
            raise CartItemsNotFoundError(user_id)

        event = CartUpdatedEvent(
            user_id=user_id, cart_data=CartPatchUpdate(total_price=0)
        )

        await self.publisher.publish(TOPIC_CART_UPDATED, event.model_dump())
        logger.info(
            f"Cart item service: CartUpdatedEvent was published for user "
            f"{user_id}'s cart"
        )
        await self.repository.delete_all_by_cart_id(cart.id)
