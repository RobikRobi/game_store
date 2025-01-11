import datetime
import typing

from sqlalchemy import text
from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


# модель таблицы с данными пользователей
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    name: Mapped[str]
    surname: Mapped[str]
    dob: Mapped[datetime.date]