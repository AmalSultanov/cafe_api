from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class CartItemModel(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id", ondelete="CASCADE"), nullable=False
    )
    meal_id: Mapped[int] = mapped_column(
        ForeignKey("meals.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    cart: Mapped["CartModel"] = relationship(
        "CartModel", back_populates="items", lazy="joined"
    )
    meal: Mapped["MealModel"] = relationship(
        "MealModel", back_populates="cart_items", lazy="joined"
    )

    repr_cols_num = 3
    repr_cols = ("created_at",)

    def __str__(self):
        return f"meal_id={self.meal_id}, quantity={self.quantity}"
