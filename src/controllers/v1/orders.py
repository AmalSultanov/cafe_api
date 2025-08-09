from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies.order import get_order_service
from src.exceptions.cart import CartNotFoundError
from src.exceptions.cart_item import CartItemsNotFoundError
from src.exceptions.order import OrdersNotFound, OrderNotFound
from src.schemas.http_error import HTTPError
from src.schemas.order import OrderRead, OrderCreate
from src.services.order.interface import IOrderService

router = APIRouter(prefix="/users", tags=["Orders"])


@router.post(
    "/{user_id}/orders",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    description="Create an order for the specified user.",
    response_description="Details of the newly created order",
    responses={
        404: {
            "model": HTTPError,
            "description": "Cart or cart items not found"
        }
    }
)
async def create_order(
    user_id: int,
    order_data: OrderCreate,
    service: IOrderService = Depends(get_order_service)
):
    try:
        return await service.create_order(user_id, order_data)
    except (CartNotFoundError, CartItemsNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.get(
    "/{user_id}/orders",
    response_model=list[OrderRead],
    description="Retrieve all user orders that they have made.",
    response_description="Details of the user's orders",
    responses={
        404: {
            "model": HTTPError,
            "description": "Orders not found for this user"
        }
    }
)
async def get_orders(
    user_id: int,
    service: IOrderService = Depends(get_order_service)
):
    try:
        return await service.get_orders(user_id)
    except OrdersNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.get(
    "/{user_id}/orders/{order_id}",
    response_model=OrderRead,
    description="Retrieve specific user order.",
    response_description="Details of the user's order",
    responses={
        404: {
            "model": HTTPError,
            "description": "Order not found for this user"
        }
    }
)
async def get_order(
    user_id: int,
    order_id: int,
    service: IOrderService = Depends(get_order_service)
):
    try:
        return await service.get_order(user_id, order_id)
    except OrderNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.delete(
    "/{user_id}/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a specific order for this user.",
    response_description="Order successfully deleted",
    responses={
        404: {
            "model": HTTPError,
            "description": "Order not found for the user"
        }
    }
)
async def delete_order(
    user_id: int,
    order_id: int,
    service: IOrderService = Depends(get_order_service)
):
    try:
        await service.delete_order(user_id, order_id)
    except OrderNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.delete(
    "/{user_id}/orders",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete all orders for this user.",
    response_description="Orders successfully deleted",
    responses={
        404: {
            "model": HTTPError,
            "description": "Orders not found for the user"
        }
    }
)
async def delete_orders(
    user_id: int,
    service: IOrderService = Depends(get_order_service)
):
    try:
        await service.delete_orders(user_id)
    except OrdersNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
