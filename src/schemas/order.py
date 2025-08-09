from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator

from src.schemas.order_item import OrderItemRead


class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentMethodEnum(str, Enum):
    CASH = "cash"
    CARD = "card"
    PAYME = "payme"
    CLICK = "click"


class OrderBase(BaseModel):
    user_id: int

    model_config = ConfigDict(
        json_encoders={Decimal: lambda v: format(v, "f")}
    )


class OrderCreate(BaseModel):
    delivery_address: str
    delivery_latitude: float
    delivery_longitude: float
    house_number: str
    entrance_number: str | None = None
    level: str | None = None
    apartment_number: str | None = None
    delivery_notes: str | None = None
    phone_number: str | None = None
    payment_method: PaymentMethodEnum
    scheduled_time: datetime | None = None

    @field_validator("delivery_latitude")
    @classmethod
    def validate_latitude(cls, latitude: float) -> float:
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return latitude

    @field_validator("delivery_longitude")
    @classmethod
    def validate_longitude(cls, longitude: float) -> float:
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return longitude


class OrderRead(OrderBase):
    id: int
    delivery_address: str
    delivery_latitude: Decimal
    delivery_longitude: Decimal
    house_number: str
    entrance_number: str | None
    level: str | None
    apartment_number: str | None
    delivery_notes: str | None
    phone_number: str | None
    total_price: Decimal
    status: OrderStatusEnum
    payment_status: str
    payment_method: str
    scheduled_time: datetime | None
    delivered_at: datetime | None
    created_at: datetime
    items: list["OrderItemRead"]

    model_config = {"from_attributes": True}
