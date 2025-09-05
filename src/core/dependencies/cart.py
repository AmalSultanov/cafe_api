from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.repositories.interfaces.cart import ICartRepository
from src.repositories.sqlalchemy.cart import SQLAlchemyCartRepository
from src.services.cart.interface import ICartService
from src.services.cart.service import CartService


def get_cart_repo(
    db: AsyncSession = Depends(get_session)
) -> ICartRepository:
    return SQLAlchemyCartRepository(db)


def get_cart_service(
    repository: ICartRepository = Depends(get_cart_repo)
) -> ICartService:
    return CartService(repository)
