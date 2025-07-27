from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.schemas.cart import CartRead


class CartModel(Base):
    __tablename__ = "carts"
    __pydantic_model__ = CartRead

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="cart", lazy="joined"
    )
    items: Mapped["CartItemModel"] = relationship(
        "CartItemModel", back_populates="cart", cascade="all, delete-orphan"
    )

    repr_cols_num = 3
    repr_cols = ("created_at",)

    def __str__(self):
        return f"Cart of user with id={self.user_id}"
