from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, HttpUrl, Field


class MealCategoryBase(BaseModel):
    name: str


class MealCategoryCreate(MealCategoryBase):
    pass


class MealCategoryRead(MealCategoryBase):
    id: int
    created_at: datetime


class MealCategoryUpdate(BaseModel):
    name: str | None = None


class MealBase(BaseModel):
    image_url: HttpUrl | None = None
    name: str
    category_id: int
    description: str
    quantity: int
    price: Decimal


class MealCreate(MealBase):
    pass


class MealRead(MealBase):
    id: int
    created_at: datetime


class MealPutUpdate(MealBase):
    pass


class MealUpdate(BaseModel):
    image_url: HttpUrl | None = None
    name: str | None = None
    category_id: int | None = None
    description: str | None = None
    quantity: int | None = Field(default=None, gt=0)
    price: Decimal | None = Field(default=None, gt=0)
