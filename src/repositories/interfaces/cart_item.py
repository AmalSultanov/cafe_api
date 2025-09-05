from typing import Protocol

from src.models.cart_item import CartItemModel


class ICartItemRepository(Protocol):
    async def create(self, cart_data: dict[str, int | float]) -> CartItemModel:
        ...

    async def get_all_by_cart_id(self, cart_id: int) -> list[CartItemModel]:
        ...

    async def get_by_id(self, item_id: int) -> CartItemModel | None: ...

    async def get_by_cart_and_item_id(
        self, cart_id: int, item_id: int
    ) -> CartItemModel | None: ...

    async def get_by_cart_and_meal_id(
        self, cart_id: int, meal_id: int
    ) -> CartItemModel | None: ...

    async def update(
        self, item_id: int, cart_data: dict[str, int | str]
    ) -> CartItemModel: ...

    async def delete_by_id(self, item_id: int) -> None: ...

    async def delete_all_by_cart_id(self, cart_id: int) -> None: ...
