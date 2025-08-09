from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.dependencies.cart import get_cart_service
from src.core.dependencies.meal import get_meal_service
from src.core.dependencies.message_broker import get_event_publisher
from src.message_broker.publisher.interface import IEventPublisher
from src.repositories.cart_item.interface import ICartItemRepository
from src.repositories.cart_item.repository import CartItemRepository
from src.services.cart.interface import ICartService
from src.services.cart_item.interface import ICartItemService
from src.services.cart_item.service import CartItemService
from src.services.meal.interface import IMealService


def get_cart_item_repo(
    db: AsyncSession = Depends(get_session)
) -> ICartItemRepository:
    return CartItemRepository(db)


def get_cart_item_service(
    repository: ICartItemRepository = Depends(get_cart_item_repo),
    cart_service: ICartService = Depends(get_cart_service),
    meal_service: IMealService = Depends(get_meal_service),
    publisher: IEventPublisher = Depends(get_event_publisher)
) -> ICartItemService:
    return CartItemService(repository, cart_service, meal_service, publisher)
