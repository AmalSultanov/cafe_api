from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict


class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderBase(BaseModel):
    user_id: int

    model_config = ConfigDict(
        json_encoders={Decimal: lambda v: format(v, "f")}
    )


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    total_price: Decimal
    status: OrderStatusEnum
    created_at: datetime
    model_config = {"from_attributes": True}
