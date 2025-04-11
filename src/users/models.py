from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # def set_password(self, password):
    #     self.password = bcrypt.generate_password_hash(password).decode(
    #         'utf-8')
    #
    # def check_password(self, password):
    #     return bcrypt.check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.id}: {self.username}>'

    def __str__(self) -> str:
        return f'User {self.id}: {self.username}, {self.email}'
