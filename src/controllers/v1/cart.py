from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies.cart import get_cart_service
from src.exceptions.cart import CartNotFoundError, CartAlreadyExistsError
from src.schemas.cart import CartRead
from src.schemas.http_error import HTTPError
from src.services.cart.interface import ICartService

router = APIRouter(prefix="/users", tags=["User Cart"])


@router.post(
    "/{user_id}/cart",
    response_model=CartRead,
    status_code=status.HTTP_201_CREATED,
    description="Create a new cart for the specified user.",
    response_description="Details of the newly created cart",
    responses={
        400: {
            "model": HTTPError,
            "description": "A cart already exists for this user"
        }
    }
)
async def create_cart(
    user_id: int,
    service: ICartService = Depends(get_cart_service)
):
    try:
        return await service.create_cart(user_id)
    except CartAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "/{user_id}/cart",
    response_model=CartRead,
    description="Retrieve the cart belonging to a specific user.",
    response_description="Details of the user's cart",
    responses={
        404: {
            "model": HTTPError,
            "description": "Cart not found for this user"
        }
    }
)
async def get_cart(
    user_id: int,
    service: ICartService = Depends(get_cart_service)
):
    try:
        return await service.get_cart_by_user_id(user_id)
    except CartNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.delete(
    "/{user_id}/cart",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete the cart associated with a specific user.",
    response_description="Cart successfully deleted",
    responses={
        404: {
            "model": HTTPError,
            "description": "Cart not found for the user"
        }
    }
)
async def delete_cart(
    user_id: int,
    service: ICartService = Depends(get_cart_service)
):
    try:
        await service.delete_cart_by_user_id(user_id)
    except CartNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
