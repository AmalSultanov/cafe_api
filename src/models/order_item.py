from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.schemas.order_item import OrderItemRead


class OrderItemModel(Base):
    __tablename__ = "order_items"
    __pydantic_model__ = OrderItemRead

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    meal_id: Mapped[int] = mapped_column(
        ForeignKey("meals.id", ondelete="SET NULL"), nullable=True
    )
    meal_name: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    order: Mapped["OrderModel"] = relationship(
        "OrderModel", back_populates="items"
    )
    meal: Mapped["MealModel"] = relationship(
        "MealModel", lazy="joined"
    )

    repr_cols_num = 3
    repr_cols = ("created_at",)

    def __str__(self):
        return f"meal_id={self.meal_id}, quantity={self.quantity}"
