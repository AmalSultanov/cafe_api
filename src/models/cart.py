from datetime import datetime

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class CartModel(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

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
