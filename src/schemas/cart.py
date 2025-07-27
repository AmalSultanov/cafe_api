from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CartBase(BaseModel):
    user_id: int

    model_config = ConfigDict(
        json_encoders={Decimal: lambda v: format(v, "f")}
    )


class CartCreate(CartBase):
    pass


class CartPatchUpdate(BaseModel):
    total_price: Decimal | None = None


class CartRead(CartBase):
    id: int
    total_price: Decimal | None
    created_at: datetime
    model_config = {"from_attributes": True}
