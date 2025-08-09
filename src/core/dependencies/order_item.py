from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.repositories.order_item.interface import IOrderItemRepository
from src.repositories.order_item.repository import OrderItemRepository
from src.services.order_item.interface import IOrderItemService
from src.services.order_item.service import OrderItemService


def get_order_item_repo(
    db: AsyncSession = Depends(get_session)
) -> IOrderItemRepository:
    return OrderItemRepository(db)


def get_order_item_service(
    repository: IOrderItemRepository = Depends(get_order_item_repo),
) -> IOrderItemService:
    return OrderItemService(repository)
