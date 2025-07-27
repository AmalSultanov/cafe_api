from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.dependencies.cart import get_cart_service
from src.repositories.order.interface import IOrderRepository
from src.repositories.order.repository import OrderRepository
from src.services.cart.interface import ICartService
from src.services.order.interface import IOrderService
from src.services.order.service import OrderService


def get_order_repo(
    db: AsyncSession = Depends(get_session)
) -> IOrderRepository:
    return OrderRepository(db)


def get_order_service(
    repository: IOrderRepository = Depends(get_order_repo),
    cart_service: ICartService = Depends(get_cart_service)
) -> IOrderService:
    return OrderService(repository, cart_service)
