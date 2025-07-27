from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator

from src.exceptions.order_item import OrderItemQuantityError


class OrderItemBase(BaseModel):
    meal_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value):
        if value is not None and value <= 0:
            raise OrderItemQuantityError()
        return value


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemPatchUpdate(BaseModel):
    quantity: int | None = None

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int):
        if value is not None and value <= 0:
            raise OrderItemQuantityError()
        return value


class OrderItemRead(OrderItemBase):
    id: int
    order_id: int
    meal_name: str
    unit_price: Decimal
    total_price: Decimal
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={Decimal: lambda v: format(v, "f")}
    )
