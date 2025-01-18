import datetime
import typing

from sqlalchemy import ForeignKey, text
from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base

import typing

if typing.TYPE_CHECKING:
    from ..seller.seller_models import SellerProfile


# модель таблицы с данными пользователей
class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    # служебная информация
    password: Mapped[bytes]

    # информация пользователя
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    surname: Mapped[str]
    dob: Mapped[datetime.date]

    profile_id:Mapped[int] = mapped_column(ForeignKey("seller_profile_table.id"), nullable=True)
    profile:Mapped["SellerProfile"] = relationship(back_populates="user", uselist=False)