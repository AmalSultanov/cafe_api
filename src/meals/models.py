from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Text, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class MealCategoryModel(Base):
    __tablename__ = 'meal_categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text('TIMEZONE("utc", now())')
    )

    meals = relationship("MealModel", back_populates='category')

    repr_cols_num = 2
    repr_cols = ('created_at',)

    def __str__(self):
        return self.name


class MealModel(Base):
    __tablename__ = 'meals'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image_url: Mapped[str | None] = mapped_column(unique=True)
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey('meal_categories.id'))
    description: Mapped[str] = mapped_column(Text)
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[Decimal]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text('TIMEZONE("utc", now())')
    )

    category = relationship("MealCategoryModel", back_populates='meals')

    repr_cols_num = 3
    repr_cols = ('created_at',)

    def __str__(self):
        return self.name
