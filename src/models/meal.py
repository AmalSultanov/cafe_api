from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Text, Integer, String, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.core.database import Base
from src.schemas.meal import MealRead


class MealModel(Base):
    __tablename__ = "meals"
    __pydantic_model__ = MealRead

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    image_url: Mapped[str | None] = mapped_column(
        String, unique=True, nullable=True
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("meal_categories.id", ondelete="CASCADE"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    category: Mapped["MealCategoryModel"] = relationship(
        "MealCategoryModel", back_populates="meals"
    )
    cart_items: Mapped["CartItemModel"] = relationship(
        "CartItemModel", back_populates="meal", cascade="all, delete-orphan"
    )

    repr_cols_num = 3
    repr_cols = ("created_at",)

    def __str__(self):
        return self.name
