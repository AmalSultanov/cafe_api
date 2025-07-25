from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, HttpUrl, Field, ConfigDict

from src.schemas.common import PaginatedBaseResponse


class MealBase(BaseModel):
    image_url: HttpUrl | None = None
    name: str
    description: str
    unit_price: Decimal

    model_config = ConfigDict(json_encoders={
        Decimal: lambda v: format(v, "f")
    })


class MealCreate(MealBase):
    pass


class MealPutUpdate(MealBase):
    pass


class MealUpdate(BaseModel):
    image_url: HttpUrl | None = None
    name: str | None = None
    description: str | None = None
    unit_price: Decimal | None = Field(default=None, gt=0)


class MealRead(MealBase):
    id: int
    category_id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class PaginatedMealResponse(PaginatedBaseResponse):
    items: list[MealRead]
