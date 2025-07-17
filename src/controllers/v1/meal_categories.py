from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies import get_meal_category_service
from src.exceptions.meal_category import (
    MealCategoryAlreadyExistsError, MealCategoryNotFoundError
)
from src.schemas.meal_category import (
    MealCategoryRead, MealCategoryCreate, MealCategoryPatchUpdate
)
from src.services.meal_category import MealCategoryService

router = APIRouter(prefix="/meal-categories", tags=["Meal Categories"])


@router.post("", response_model=MealCategoryRead)
async def create_category(
    category_data: MealCategoryCreate,
    service: MealCategoryService = Depends(get_meal_category_service)
):
    try:
        return await service.create_category(category_data)
    except MealCategoryAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("", response_model=list[MealCategoryRead])
async def get_categories(
    service: MealCategoryService = Depends(get_meal_category_service)
):
    return await service.get_categories()


@router.get("/{category_id}", response_model=MealCategoryRead)
async def get_category(
    category_id: int,
    service: MealCategoryService = Depends(get_meal_category_service)
):
    try:
        return await service.get_category(category_id)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.patch(
    "/{category_id}", response_model=MealCategoryRead
)
async def update_category(
    category_id: int,
    category_data: MealCategoryPatchUpdate,
    service: MealCategoryService = Depends(get_meal_category_service)
):
    try:
        return await service.update_category(category_id, category_data)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealCategoryAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    service: MealCategoryService = Depends(get_meal_category_service)
):
    try:
        return await service.delete_category(category_id)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
