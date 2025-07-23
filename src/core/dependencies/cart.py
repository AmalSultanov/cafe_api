from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.repositories.cart.interface import ICartRepository
from src.repositories.cart.repository import CartRepository
from src.services.cart.interface import ICartService
from src.services.cart.service import CartService


def get_cart_repo(
    db: AsyncSession = Depends(get_session)
) -> ICartRepository:
    return CartRepository(db)


def get_cart_service(
    repository: ICartRepository = Depends(get_cart_repo)
) -> ICartService:
    return CartService(repository)
