from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, HttpUrl, ConfigDict, field_validator

from src.exceptions.meal import MealPriceError
from src.schemas.common import PaginatedBaseResponse


class MealBase(BaseModel):
    image_url: HttpUrl | None = None
    name: str
    description: str
    unit_price: Decimal

    model_config = ConfigDict(json_encoders={
        Decimal: lambda v: format(v, "f")
    })

    @field_validator("unit_price")
    @classmethod
    def validate_unit_price(cls, value: Decimal):
        if value <= 0:
            raise MealPriceError()
        return value


class MealCreate(MealBase):
    pass


class MealPutUpdate(MealBase):
    pass


class MealPatchUpdate(BaseModel):
    image_url: HttpUrl | None = None
    name: str | None = None
    description: str | None = None
    unit_price: Decimal | None = None

    @field_validator("unit_price")
    @classmethod
    def validate_unit_price(cls, value: Decimal | None):
        if value is not None and value <= 0:
            raise MealPriceError()
        return value


class MealRead(MealBase):
    id: int
    category_id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class PaginatedMealResponse(PaginatedBaseResponse):
    items: list[MealRead]
