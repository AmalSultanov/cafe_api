from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Enum, Numeric, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base
import enum

from src.models.order_item import OrderItemModel
from src.schemas.order import OrderRead


class OrderStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethodEnum(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    PAYME = "payme"
    CLICK = "click"


class OrderModel(Base):
    __tablename__ = "orders"
    __pydantic_model__ = OrderRead

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    cart_id: Mapped[int] = mapped_column(Integer, nullable=False)
    delivery_address: Mapped[str] = mapped_column(String, nullable=False)
    delivery_latitude: Mapped[Decimal] = mapped_column(
        Numeric(10, 8), nullable=False
    )
    delivery_longitude: Mapped[Decimal] = mapped_column(
        Numeric(11, 8), nullable=False
    )
    house_number: Mapped[str] = mapped_column(String, nullable=False)
    entrance_number: Mapped[str | None] = mapped_column(String, nullable=True)
    level: Mapped[str | None] = mapped_column(String, nullable=True)
    apartment_number: Mapped[str | None] = mapped_column(String, nullable=True)
    delivery_notes: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    status: Mapped[OrderStatusEnum] = mapped_column(
        Enum(OrderStatusEnum, name="order_status_enum"),
        default=OrderStatusEnum.PENDING, nullable=False
    )
    payment_status: Mapped[PaymentStatusEnum] = mapped_column(
        Enum(PaymentStatusEnum, name="payment_status_enum"),
        default=PaymentStatusEnum.PENDING, nullable=False
    )
    payment_method: Mapped[PaymentMethodEnum] = mapped_column(
        Enum(PaymentMethodEnum, name="payment_method_enum"),
        nullable=False
    )
    scheduled_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    items: Mapped[list["OrderItemModel"]] = relationship(
        "OrderItemModel", back_populates="order", cascade="all, delete-orphan"
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="orders", lazy="joined"
    )

    repr_cols_num = 3
    repr_cols = ("created_at",)

    def __str__(self):
        return f"Order of user with id={self.user_id}"
