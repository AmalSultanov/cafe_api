from typing import Protocol

from src.models.cart import CartModel


class ICartRepository(Protocol):
    async def create(self, user_id: int) -> CartModel:
        ...

    async def get_by_user_id(self, user_id: int) -> CartModel | None:
        ...

    async def update(
        self, user_id: int, cart_data: dict[str, str]
    ) -> CartModel | None: ...

    async def delete(self, cart_id: int) -> None:
        ...
