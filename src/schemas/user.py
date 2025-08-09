from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator

from src.exceptions.user import UserPhoneError
from src.schemas.common import PaginatedBaseResponse


class ProviderEnum(str, Enum):
    telegram = "telegram"
    web = "web"


class IdentityBase(BaseModel):
    provider: ProviderEnum
    provider_id: str
    username: str


class IdentityCheck(BaseModel):
    provider: ProviderEnum
    provider_id: str
    username: str | None = None


class IdentityCreate(IdentityBase):
    pass


class IdentityRead(IdentityBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class IdentityStatusResponse(BaseModel):
    status: str


class UserBase(BaseModel):
    name: str | None
    surname: str | None
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, phone_number: str) -> str:
        if not phone_number.isdigit():
            raise UserPhoneError()
        return phone_number


class UserRegister(UserBase, IdentityBase):
    pass


class UserPutUpdate(UserBase):
    name: str
    surname: str


class UserPatchUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    phone_number: str | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, phone_number: str) -> str:
        if not phone_number.isdigit():
            raise UserPhoneError()
        return phone_number


class UserRead(UserBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class PaginatedUserResponse(PaginatedBaseResponse):
    items: list[UserRead]


class UserWithTokens(BaseModel):
    user: UserRead
    access_token: str
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class LogoutResponse(BaseModel):
    message: str
