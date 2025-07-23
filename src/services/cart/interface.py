from typing import Protocol

from src.schemas.cart import CartRead


class ICartService(Protocol):
    async def create_cart(self, user_id: int) -> CartRead: ...

    async def get_cart_by_user_id(self, user_id: int) -> CartRead: ...

    async def delete_cart_by_user_id(self, user_id: int) -> None: ...
