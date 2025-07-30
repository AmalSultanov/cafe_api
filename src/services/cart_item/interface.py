from typing import Protocol

from src.schemas.cart_item import (
    CartItemCreate, CartItemPatchUpdate, CartItemRead
)


class ICartItemService(Protocol):
    async def add_item_to_cart(
        self, user_id: int, item_data: CartItemCreate
    ) -> CartItemRead:
        ...

    async def get_cart_items(self, user_id: int) -> list[CartItemRead]:
        ...

    async def get_cart_item(self, user_id: int, item_id: int) -> CartItemRead:
        ...

    async def update_cart_item(
        self,
        user_id: int,
        item_id: int,
        item_data: CartItemPatchUpdate
    ) -> CartItemRead:
        ...

    async def remove_item_from_cart(self, user_id: int, item_id: int) -> None:
        ...

    async def remove_items_from_cart(self, user_id: int) -> None:
        ...
