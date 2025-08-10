from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies.meal_category import get_meal_category_service
from src.core.logging import logger
from src.exceptions.meal_category import (
    MealCategoryAlreadyExistsError, MealCategoryNotFoundError,
    NoMealCategoryUpdateDataError
)
from src.schemas.common import PaginationParams
from src.schemas.http_error import HTTPError
from src.schemas.meal_category import (
    MealCategoryRead, MealCategoryCreate, MealCategoryPatchUpdate,
    PaginatedMealCategoryResponse
)
from src.services.meal_category.interface import IMealCategoryService

router = APIRouter(prefix="/meal-categories", tags=["Meal Categories"])


@router.post(
    "",
    response_model=MealCategoryRead,
    status_code=status.HTTP_201_CREATED,
    description="Create a new meal category with a unique name.",
    response_description="Details of the created meal category",
    responses={
        409: {
            "model": HTTPError,
            "description": "Meal category already exists"
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def create_category(
    category_data: MealCategoryCreate,
    service: IMealCategoryService = Depends(get_meal_category_service)
):
    logger.info(f"API request: Create meal category '{category_data.name}'")
    try:
        result = await service.create_category(category_data)
        logger.info(
            f"API response: Meal category created with ID: {result.id}"
        )
        return result
    except MealCategoryAlreadyExistsError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@router.get(
    "",
    response_model=PaginatedMealCategoryResponse,
    description=(
        "Retrieve a paginated list of all existing meal categories. Supports "
        "`page` (page number) and `per_page` (page size) query parameters."
    ),
    response_description="Paginated list of meal categories"
)
async def get_categories(
    pagination_params: PaginationParams = Depends(PaginationParams),
    service: IMealCategoryService = Depends(get_meal_category_service)
):
    logger.info(
        f"API request: Get meal categories - page: {pagination_params.page}, "
        f"per_page: {pagination_params.per_page}"
    )
    try:
        result = await service.get_categories(pagination_params)
        logger.info(
            f"API response: Retrieved {len(result.categories)} meal categories"
        )
        return result
    except Exception as e:
        logger.error(f"API error: Failed to get meal categories: {e}")
        raise


@router.get(
    "/{category_id}",
    response_model=MealCategoryRead,
    description="Retrieve details of a specific meal category by its ID.",
    response_description="Meal category details",
    responses={
        404: {
            "model": HTTPError,
            "description": "Meal category not found"
        }
    }
)
async def get_category(
    category_id: int,
    service: IMealCategoryService = Depends(get_meal_category_service)
):
    logger.info(f"API request: Get meal category {category_id}")
    try:
        result = await service.get_category(category_id)
        logger.info(f"API response: Meal category {category_id} was retrieved")
        return result
    except MealCategoryNotFoundError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.patch(
    "/{category_id}",
    response_model=MealCategoryRead,
    description="Partially update an existing meal category using its ID.",
    response_description="Updated meal category",
    responses={
        400: {
            "model": HTTPError,
            "description": "No update data"
        },
        409: {
            "model": HTTPError,
            "description": "Meal category name already exists"
        },
        404: {
            "model": HTTPError,
            "description": "Meal category not found"
        }
    }
)
async def update_category(
    category_id: int,
    category_data: MealCategoryPatchUpdate,
    service: IMealCategoryService = Depends(get_meal_category_service)
):
    logger.info(f"API request: Update meal category {category_id}")
    try:
        result = await service.update_category(category_id, category_data)
        logger.info(f"API response: Meal category {category_id} was updated")
        return result
    except NoMealCategoryUpdateDataError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except MealCategoryNotFoundError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealCategoryAlreadyExistsError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a specific meal category by its ID.",
    response_description="Meal category successfully deleted",
    responses={
        404: {
            "model": HTTPError,
            "description": "Meal category not found"
        }
    }
)
async def delete_category(
    category_id: int,
    service: IMealCategoryService = Depends(get_meal_category_service)
):
    logger.info(f"API request: Delete meal category {category_id}")
    try:
        result = await service.delete_category(category_id)
        logger.info(f"API response: Meal category {category_id} was deleted")
        return result
    except MealCategoryNotFoundError as e:
        logger.warning(f"API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
