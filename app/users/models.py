from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base

if TYPE_CHECKING:
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    admin: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return f"Пользователь {self.email}"
