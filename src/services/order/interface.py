from typing import Protocol

from src.schemas.order import OrderRead, OrderCreate


class IOrderService(Protocol):
    async def create_order(
        self, user_id: int, order_data: OrderCreate
    ) -> OrderRead: ...

    async def get_orders(self, user_id: int) -> list[OrderRead]: ...

    async def get_order(self, user_id: int, order_id: int) -> OrderRead: ...

    async def delete_order(self, user_id: int, order_id: int) -> None: ...

    async def delete_orders(self, user_id: int) -> None: ...
