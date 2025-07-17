from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class MealBase(BaseModel):
    image_url: HttpUrl | None = None
    name: str
    description: str
    price: Decimal

    model_config = ConfigDict(json_encoders={
        Decimal: lambda v: format(v, "f")
    })


class MealCreate(MealBase):
    pass


class MealRead(MealBase):
    id: int
    category_id: int
    created_at: datetime


class MealPutUpdate(MealBase):
    pass


class MealUpdate(BaseModel):
    image_url: HttpUrl | None = None
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
