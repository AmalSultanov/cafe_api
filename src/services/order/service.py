from src.core.utils.datetime import strip_timezone
from src.exceptions.cart import CartNotFoundError
from src.exceptions.cart_item import CartItemsNotFoundError
from src.exceptions.order import OrdersNotFound, OrderNotFound
from src.repositories.order.interface import IOrderRepository
from src.schemas.order import OrderRead, OrderCreate
from src.services.cart.interface import ICartService
from src.services.cart_item.interface import ICartItemService
from src.services.order_item.interface import IOrderItemService


class OrderService:
    def __init__(
        self,
        repository: IOrderRepository,
        cart_service: ICartService,
        cart_item_service: ICartItemService,
        order_item_service: IOrderItemService
    ) -> None:
        self.repository = repository
        self.cart_service = cart_service
        self.cart_item_service = cart_item_service
        self.order_item_service = order_item_service

    async def create_order(
        self, user_id: int, order_data: OrderCreate
    ) -> OrderRead:
        cart = await self.cart_service.get_cart_by_user_id(user_id)
        if not cart:
            raise CartNotFoundError(user_id)

        cart_items = await self.cart_item_service.get_cart_items(user_id)
        if not cart_items:
            raise CartItemsNotFoundError(user_id)

        order_dict = order_data.model_dump()
        order_dict.update({
            "cart_id": cart.id,
            "total_price": cart.total_price,
            "scheduled_time": strip_timezone(order_data.scheduled_time)
        })
        items_data = [
            {
                "meal_id": cart_item.meal_id,
                "quantity": cart_item.quantity,
                "meal_name": cart_item.meal_name,
                "unit_price": cart_item.unit_price,
                "total_price": cart_item.total_price
            }
            for cart_item in cart_items
        ]
        order = await self.repository.create_with_items(
            user_id, order_dict, items_data
        )

        await self.cart_item_service.remove_items_from_cart(user_id)
        return OrderRead.model_validate(order)

    async def get_orders(self, user_id: int) -> list[OrderRead]:
        orders = await self.repository.get_all(user_id)
        return [OrderRead.model_validate(order) for order in orders]

    async def get_order(self, user_id: int, order_id: int) -> OrderRead:
        order = await self.repository.get_by_user_and_order_id(
            user_id, order_id
        )

        if not order:
            raise OrderNotFound(user_id, order_id)
        return OrderRead.model_validate(order)

    async def delete_order(self, user_id: int, order_id: int) -> None:
        try:
            await self.get_order(user_id, order_id)
        except OrderNotFound:
            raise

        await self.repository.delete_one(user_id, order_id)

    async def delete_orders(self, user_id: int) -> None:
        try:
            await self.get_orders(user_id)
        except OrdersNotFound:
            raise

        await self.repository.delete_all(user_id)
