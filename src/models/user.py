import enum
from datetime import datetime

from sqlalchemy import (
    ForeignKey, UniqueConstraint, Enum, Integer, String, DateTime
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.core.database import Base
from src.schemas.user import UserRead, IdentityRead


class IdentityProviderEnum(enum.Enum):
    telegram = "telegram"
    web = "web"


class UserModel(Base):
    __tablename__ = "users"
    __pydantic_model__ = UserRead

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    surname: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_number: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    identities: Mapped[list["UserIdentityModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    cart: Mapped["CartModel"] = relationship(
        "CartModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    orders: Mapped[list["OrderModel"]] = relationship(
        "OrderModel", back_populates="user", cascade="all, delete-orphan"
    )

    repr_cols_num = 2
    repr_cols = ("created_at",)

    def __str__(self):
        return self.name


class UserIdentityModel(Base):
    __tablename__ = "user_identities"
    __table_args__ = (
        UniqueConstraint(
            "provider", "provider_id", name="uq_provider_provider_id"
        ),
        UniqueConstraint(
            "provider", "username", name="uq_provider_username"
        )
    )
    __pydantic_model__ = IdentityRead

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[IdentityProviderEnum] = mapped_column(
        Enum(IdentityProviderEnum, name="identity_provider_enum")
    )
    provider_id: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    user: Mapped[UserModel] = relationship(back_populates="identities")

    repr_cols_num = 2
    repr_cols = ("created_at",)

    def __str__(self):
        return f"{self.provider} user with provider_id={self.provider_id}"
