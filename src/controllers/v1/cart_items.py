from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies.cart_item import get_cart_item_service
from src.core.logging import logger
from src.exceptions.cart import CartNotFoundError
from src.exceptions.cart_item import (
    CartItemNotFoundError, CartItemsNotFoundError, NoCartItemUpdateDataError,
    CartItemQuantityError
)
from src.exceptions.meal import MealNotFoundError
from src.schemas.cart_item import (
    CartItemRead, CartItemCreate, CartItemPatchUpdate
)
from src.schemas.http_error import HTTPError
from src.services.cart_item.interface import ICartItemService

router = APIRouter(prefix="/users", tags=["Cart Items"])


@router.post(
    "/{user_id}/cart/items",
    response_model=CartItemRead,
    status_code=status.HTTP_201_CREATED,
    description=(
        "Add a new item to the user's cart. "
        "Cart should exist, otherwise exception will be triggered."
    ),
    response_description="Details of the newly added cart item",
    responses={
        400: {
            "model": HTTPError,
            "description": "Incorrect quantity value"
        },
        404: {
            "model": HTTPError,
            "description": (
                "Cart not found for the given user or meal not found"
            )
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def add_item_to_cart(
    user_id: int,
    item_data: CartItemCreate,
    service: ICartItemService = Depends(get_cart_item_service)
):
    logger.info(
        f"API request: Add item to cart for user {user_id}, "
        f"meal_id: {item_data.meal_id}"
    )
    try:
        result = await service.add_item_to_cart(user_id, item_data)
        logger.info(
            f"API response: Item was added to cart for user {user_id}"
        )
        return result
    except (CartNotFoundError, MealNotFoundError) as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except CartItemQuantityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "/{user_id}/cart/items",
    response_model=list[CartItemRead],
    description="Retrieve all items currently in the user's cart.",
    response_description="List of items in the cart",
    responses={
        404: {
            "model": HTTPError,
            "description": "Cart not found for the given user"
        }
    }
)
async def get_cart_items(
    user_id: int,
    service: ICartItemService = Depends(get_cart_item_service)
):
    logger.info(f"API request: Get cart items for user {user_id}")
    try:
        result = await service.get_cart_items(user_id)
        logger.info(
            f"API response: Got {len(result)} cart items for user {user_id}"
        )
        return result
    except CartNotFoundError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.get(
    "/{user_id}/cart/items/{item_id}",
    response_model=CartItemRead,
    description="Fetch a specific item from the user's cart using its ID.",
    response_description="Details of the cart item",
    responses={
        404: {
            "model": HTTPError,
            "description": "Cart or cart item not found"
        }
    }
)
async def get_cart_item(
    user_id: int,
    item_id: int,
    service: ICartItemService = Depends(get_cart_item_service)
):
    logger.info(f"API request: Get cart item {item_id} for user {user_id}")
    try:
        result = await service.get_cart_item(user_id, item_id)
        logger.info(
            f"API response: Cart item {item_id} was retrieved for user {user_id}"
        )
        return result
    except (CartNotFoundError, CartItemNotFoundError) as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.patch(
    "/{user_id}/cart/items/{item_id}",
    response_model=CartItemRead | None,
    description=(
        "Update one or more fields of a specific cart item. "
        "Only the fields that need to be updated must be provided. "
        "If quantity is set to 0, this item will be removed from cart."
    ),
    response_description="Details of the updated cart item",
    responses={
        400: {
            "model": HTTPError,
            "description": "No data to update or incorrect quantity value"
        },
        404: {
            "model": HTTPError,
            "description": "Cart or cart item not found"
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def update_cart_item(
    user_id: int,
    item_id: int,
    item_data: CartItemPatchUpdate,
    service: ICartItemService = Depends(get_cart_item_service)
):
    logger.info(f"API request: Update cart item {item_id} for user {user_id}")
    try:
        result = await service.update_cart_item(user_id, item_id, item_data)
        logger.info(
            f"API response: Cart item {item_id} was updated for user {user_id}"
        )
        return result
    except (NoCartItemUpdateDataError, CartItemQuantityError) as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except (CartNotFoundError, CartItemNotFoundError) as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.delete(
    "/{user_id}/cart/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Remove a specific item from the user's cart.",
    response_description="Cart item successfully removed",
    responses={
        404: {
            "model": HTTPError,
            "description": "Cart or cart item not found"
        }
    }
)
async def delete_cart_item(
    user_id: int,
    item_id: int,
    service: ICartItemService = Depends(get_cart_item_service)
):
    logger.info(f"API request: Delete cart item {item_id} for user {user_id}")
    try:
        await service.remove_item_from_cart(user_id, item_id)
        logger.info(
            f"API response: Cart item {item_id} was deleted for user {user_id}"
        )
    except (CartNotFoundError, CartItemNotFoundError) as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.delete(
    "/{user_id}/cart/items",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Remove all items from the user's cart.",
    response_description="All cart items successfully removed",
    responses={
        404: {
            "model": HTTPError,
            "description": "Cart not found or cart is already empty"
        }
    }
)
async def delete_cart_items(
    user_id: int,
    service: ICartItemService = Depends(get_cart_item_service)
):
    logger.info(f"API request: Delete all cart items for user {user_id}")
    try:
        await service.remove_items_from_cart(user_id)
        logger.info(
            f"API response: All cart items were deleted for user {user_id}"
        )
    except (CartNotFoundError, CartItemsNotFoundError) as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
