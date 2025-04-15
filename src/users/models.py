from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    phone_number: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    telegram_link: Mapped['TelegramUserLinkModel'] = relationship(
        back_populates='user'
    )

    repr_cols_num = 2
    repr_cols = ('created_at',)

    def __str__(self):
        return self.name


class TelegramUserLinkModel(Base):
    __tablename__ = 'telegram_user_links'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_user_id: Mapped[int] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped['UserModel'] = relationship(back_populates='telegram_link')

    repr_cols_num = 2
    repr_cols = ('created_at',)
