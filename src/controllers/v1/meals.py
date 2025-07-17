from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import get_meal_service
from src.exceptions.meal import MealNotFoundError, MealAlreadyExistsError
from src.exceptions.meal_category import MealCategoryNotFoundError
from src.schemas.meal import (
    MealRead, MealCreate, MealUpdate, MealPutUpdate
)
from src.services.meal import MealService


router = APIRouter(prefix="/meal-categories", tags=["Meals"])


@router.post("/{category_id}/meals", response_model=MealRead)
async def create_meal(
    category_id: int,
    meal_data: MealCreate,
    service: MealService = Depends(get_meal_service)
):
    try:
        return await service.create_meal(category_id, meal_data)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/{category_id}/meals", response_model=list[MealRead])
async def get_meals(
    category_id: int, service: MealService = Depends(get_meal_service)
):
    try:
        return await service.get_meals_by_category_id(category_id)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.get("/{category_id}/meals/{meal_id}", response_model=MealRead)
async def get_meal(
    category_id: int,
    meal_id: int,
    service: MealService = Depends(get_meal_service)
):
    try:
        return await service.get_meal(category_id, meal_id)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.put("/{category_id}/meals/{meal_id}", response_model=MealRead)
async def update_meal(
    category_id: int,
    meal_id: int,
    meal_data: MealPutUpdate,
    service: MealService = Depends(get_meal_service)
):
    try:
        return await service.update_meal(category_id, meal_id, meal_data)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.patch("/{category_id}/meals/{meal_id}", response_model=MealRead)
async def partial_update_meal(
    category_id: int,
    meal_id: int,
    meal_data: MealUpdate,
    service: MealService = Depends(get_meal_service)
):
    try:
        return await service.update_meal(category_id, meal_id, meal_data, True)
    except MealCategoryNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except MealNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.delete("/{category_id}/meals/{meal_id}", status_code=204)
async def delete_meal(
    category_id: int,
    meal_id: int,
    service: MealService = Depends(get_meal_service)
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
