from datetime import datetime

from pydantic import BaseModel

from src.schemas.common import PaginatedBaseResponse


class MealCategoryBase(BaseModel):
    name: str


class MealCategoryCreate(MealCategoryBase):
    pass


class MealCategoryPatchUpdate(BaseModel):
    name: str | None = None


class MealCategoryRead(MealCategoryBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class PaginatedMealCategoryResponse(PaginatedBaseResponse):
    items: list[MealCategoryRead]
