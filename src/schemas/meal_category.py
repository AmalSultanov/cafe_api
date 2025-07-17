from datetime import datetime

from pydantic import BaseModel


class MealCategoryBase(BaseModel):
    name: str


class MealCategoryCreate(MealCategoryBase):
    pass


class MealCategoryRead(MealCategoryBase):
    id: int
    created_at: datetime


class MealCategoryPatchUpdate(BaseModel):
    name: str | None = None
