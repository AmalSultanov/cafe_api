from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.core.database import Base
from src.schemas.meal_category import MealCategoryRead


class MealCategoryModel(Base):
    __tablename__ = "meal_categories"
    __pydantic_model__ = MealCategoryRead

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    meals: Mapped["MealModel"] = relationship(
        "MealModel", back_populates="category"
    )

    repr_cols_num = 2
    repr_cols = ("created_at",)

    def __str__(self):
        return self.name
