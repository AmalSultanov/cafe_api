from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator

from src.exceptions.cart_item import CartItemQuantityError


class CartItemBase(BaseModel):
    meal_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value):
        if value is not None and value <= 0:
            raise CartItemQuantityError()
        return value


class CartItemPatchUpdate(BaseModel):
    quantity: int | None = None

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int):
        if value is not None and value < 0:
            raise CartItemQuantityError()
        return value


class CartItemRead(CartItemBase):
    id: int
    meal_name: str
    unit_price: Decimal
    total_price: Decimal
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={Decimal: lambda v: format(v, "f")}
    )
