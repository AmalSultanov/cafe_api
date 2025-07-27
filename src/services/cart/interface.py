from typing import Protocol

from src.schemas.cart import CartRead, CartPatchUpdate


class ICartService(Protocol):
    async def create_cart(self, user_id: int) -> CartRead: ...

    async def get_cart_by_user_id(self, user_id: int) -> CartRead: ...

    async def update_cart(
        self, user_id: int, cart_data: CartPatchUpdate
    ) -> CartRead: ...

    async def delete_cart_by_user_id(self, user_id: int) -> None: ...
