from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies.meal import get_meal_service
from src.exceptions.meal import (
    MealNotFoundError, MealAlreadyExistsError, NoMealUpdateDataError,
    MealPriceError
)
from src.exceptions.meal_category import MealCategoryNotFoundError
from src.schemas.common import PaginationParams
from src.schemas.http_error import HTTPError
from src.schemas.meal import (
    MealRead, MealCreate, MealPatchUpdate, MealPutUpdate, PaginatedMealResponse
)
from src.services.meal.interface import IMealService

router = APIRouter(prefix="/meal-categories", tags=["Meals"])


@router.post(
    "/{category_id}/meals",
    response_model=MealRead,
    status_code=status.HTTP_201_CREATED,
    description=(
        "Create a new meal under the specified category. "
        "The meal name must be unique."
    ),
    response_description="Details of the newly created meal",
    responses={
        400: {
            "model": HTTPError,
            "description": "Unit price must be greater than 0"
        },
        404: {
            "model": HTTPError,
            "description": "Meal category not found"
        },
        409: {
            "model": HTTPError,
            "description": "Meal with the given name already exists"
        },
        422: {"description": "Invalid input format or missing fields"}
    }
)
async def create_meal(
    category_id: int,
    meal_data: MealCreate,
    service: IMealService = Depends(get_meal_service)
):
    try:
        return await service.create_meal(category_id, meal_data)
    except MealPriceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@router.get(
    "/{category_id}/meals",
    response_model=PaginatedMealResponse,
    description=(
        "Fetch a paginated list of all meals that belong to the specified "
        "meal category. Supports `page` (page number) and "
        "`per_page` (page size) query parameters. `total` field in response "
        "indicates the total items in this particular category."
    ),
    response_description="Paginated list of meals in the category",
    responses={
        404: {
            "model": HTTPError,
            "description": "Meal category not found"
        }
    }
)
async def get_meals(
    category_id: int,
    pagination_params: PaginationParams = Depends(PaginationParams),
    service: IMealService = Depends(get_meal_service)
):
    try:
        return await service.get_meals_by_category_id(
            category_id, pagination_params
        )
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.get(
    "/{category_id}/meals/{meal_id}",
    response_model=MealRead,
    description=(
        "Retrieve details of a specific meal under a given category by IDs."
    ),
    response_description="Details of the requested meal",
    responses={
        404: {
            "model": HTTPError,
            "description": "Meal or category not found"
        }
    }
)
async def get_meal(
    category_id: int,
    meal_id: int,
    service: IMealService = Depends(get_meal_service)
):
    try:
        return await service.get_meal(meal_id, category_id)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.put(
    "/{category_id}/meals/{meal_id}",
    response_model=MealRead,
    description=(
        "Completely update a meal with new data. "
        "All required fields must be provided."
    ),
    response_description="Details of the updated meal",
    responses={
        400: {
            "model": HTTPError,
            "description": (
                "No meal data to update or unit price is not greater than 0"
            )
        },
        404: {
            "model": HTTPError,
            "description": "Meal or category not found"
        },
        409: {
            "model": HTTPError,
            "description": "Provided meal name already exists"
        },
        422: {"description": "Invalid request format"}
    }
)
async def update_meal(
    category_id: int,
    meal_id: int,
    meal_data: MealPutUpdate,
    service: IMealService = Depends(get_meal_service)
):
    try:
        return await service.update_meal(category_id, meal_id, meal_data)
    except MealPriceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except NoMealUpdateDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@router.patch(
    "/{category_id}/meals/{meal_id}",
    response_model=MealRead,
    description=(
        "Update one or more fields of a specific meal. "
        "Only the fields that need to be updated must be provided."
    ),
    response_description="Details of the partially updated meal",
    responses={
        400: {
            "model": HTTPError,
            "description": (
                "No meal data to update or unit price is not greater than 0"
            )
        },
        404: {
            "model": HTTPError,
            "description": "Meal or category not found"
        },
        409: {
            "model": HTTPError,
            "description": "Provided meal name already exists"
        }
    }
)
async def partial_update_meal(
    category_id: int,
    meal_id: int,
    meal_data: MealPatchUpdate,
    service: IMealService = Depends(get_meal_service)
):
    try:
        return await service.update_meal(category_id, meal_id, meal_data, True)
    except MealPriceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except NoMealUpdateDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@router.delete(
    "/{category_id}/meals/{meal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a meal from a given category by their IDs.",
    response_description="Meal successfully deleted",
    responses={
        404: {
            "model": HTTPError,
            "description": "Meal or category not found"
        }
    }
)
async def delete_meal(
    category_id: int,
    meal_id: int,
    service: IMealService = Depends(get_meal_service)
):
    try:
        await service.delete_meal(category_id, meal_id)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
