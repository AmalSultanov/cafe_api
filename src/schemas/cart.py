from datetime import datetime

from pydantic import BaseModel


class CartBase(BaseModel):
    user_id: int


class CartCreate(CartBase):
    pass


class CartRead(CartBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}
