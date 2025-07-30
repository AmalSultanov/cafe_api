from src.exceptions.cart import CartNotFoundError
from src.exceptions.cart_item import (
    CartItemNotFoundError, CartItemsNotFoundError, NoCartItemUpdateDataError
)
from src.message_broker.config import broker
from src.message_broker.events.cart import CartUpdatedEvent
from src.message_broker.publisher import EventPublisher
from src.message_broker.topics import TOPIC_CART_UPDATED
from src.repositories.cart_item.interface import ICartItemRepository
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
        meal_service: IMealService
    ) -> None:
        self.repository = repository
        self.cart_service = cart_service
        self.meal_service = meal_service

    async def add_item_to_cart(
        self, user_id: int, item_data: CartItemCreate
    ) -> CartItemRead:
        try:
            cart = await self.cart_service.get_cart_by_user_id(user_id)
        except CartNotFoundError:
            raise

        existing_item = await self.repository.get_by_cart_and_meal_id(
            cart.id, item_data.meal_id
        )
        if existing_item:
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
        item = await self.repository.create(item_dict)
        event = CartUpdatedEvent(
            user_id=user_id,
            cart_data=CartPatchUpdate(
                total_price=cart.total_price + item_dict["total_price"]
            )
        )

        publisher = EventPublisher(broker)

        await publisher.publish(TOPIC_CART_UPDATED, event.model_dump())
        return CartItemRead.model_validate(item)

    async def get_cart_items(self, user_id: int) -> list[CartItemRead]:
        cart = await self.cart_service.get_cart_by_user_id(user_id)
        if not cart:
            raise CartNotFoundError(user_id)

        items = await self.repository.get_all_by_cart_id(cart.id)
        return [CartItemRead.model_validate(item) for item in items]

    async def get_cart_item(self, user_id: int, item_id: int) -> CartItemRead:
        cart = await self.cart_service.get_cart_by_user_id(user_id)
        if not cart:
            raise CartNotFoundError(user_id)

        item = await self.repository.get_by_id(item_id)
        if item is None or item.cart_id != cart.id:
            raise CartItemNotFoundError(item_id)

        return CartItemRead.model_validate(item)

    async def update_cart_item(
        self,
        user_id: int,
        item_id: int,
        item_data: CartItemPatchUpdate
    ) -> CartItemRead:
        new_data = item_data.model_dump(exclude_unset=True)
        if not new_data:
            raise NoCartItemUpdateDataError()

        cart = await self.cart_service.get_cart_by_user_id(user_id)
        if not cart:
            raise CartNotFoundError(user_id)

        item = await self.repository.get_by_id(item_id)
        if not item or item.cart_id != cart.id:
            raise CartItemNotFoundError(item_id)

        if "quantity" in new_data:
            quantity = new_data["quantity"]
            new_total_price = item.unit_price * quantity
            new_data["total_price"] = new_total_price
            event = CartUpdatedEvent(
                user_id=user_id,
                cart_data=CartPatchUpdate(
                    total_price=cart.total_price - item.total_price + new_total_price
                )
            )

            publisher = EventPublisher(broker)
            await publisher.publish(TOPIC_CART_UPDATED, event.model_dump())

        upd_item = await self.repository.update(item_id, new_data)
        return CartItemRead.model_validate(upd_item)

    async def remove_item_from_cart(self, user_id: int, item_id: int) -> None:
        cart = await self.cart_service.get_cart_by_user_id(user_id)
        if not cart:
            raise CartNotFoundError(user_id)

        item = await self.repository.get_by_cart_and_item_id(
            cart.id, item_id
        )
        if not item:
            raise CartItemNotFoundError(item_id)

        event = CartUpdatedEvent(
            user_id=user_id,
            cart_data=CartPatchUpdate(
                total_price=cart.total_price-item.total_price
            )
        )
        publisher = EventPublisher(broker)
        await publisher.publish(TOPIC_CART_UPDATED, event.model_dump())
        await self.repository.delete_by_id(item.id)

    async def remove_items_from_cart(self, user_id: int) -> None:
        cart = await self.cart_service.get_cart_by_user_id(user_id)
        if not cart:
            raise CartNotFoundError(user_id)

        items = await self.repository.get_all_by_cart_id(cart.id)
        if not items:
            raise CartItemsNotFoundError(user_id)

        event = CartUpdatedEvent(
            user_id=user_id, cart_data=CartPatchUpdate(total_price=0)
        )
        publisher = EventPublisher(broker)
        await publisher.publish(TOPIC_CART_UPDATED, event.model_dump())
        await self.repository.delete_all_by_cart_id(cart.id)
