from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ProviderEnum(str, Enum):
    telegram = "telegram"
    web = "web"


class UserBase(BaseModel):
    name: str | None
    surname: str | None
    phone_number: str


class IdentityBase(BaseModel):
    provider: ProviderEnum
    provider_id: str
    username: str | None


class UserRegister(UserBase, IdentityBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime


class UserUpdate(UserBase):
    pass


class UserPartialUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    phone_number: str | None = None


class IdentityCheck(IdentityBase):
    pass
