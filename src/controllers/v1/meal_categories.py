from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies.meal_category import get_meal_category_service
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
        400: {
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
    try:
        return await service.create_category(category_data)
    except MealCategoryAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
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
    return await service.get_categories(pagination_params)


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
    try:
        return await service.get_category(category_id)
    except MealCategoryNotFoundError as e:
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
            "description": "No update data or category name already exists"
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
    try:
        return await service.update_category(category_id, category_data)
    except NoMealCategoryUpdateDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealCategoryAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
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
    try:
        return await service.delete_category(category_id)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
