import datetime
import typing

from sqlalchemy import ForeignKey
from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
    from .seller_models.SellerProductModel import SellerProfile
    from .seller_models.SellerProductModel import Review, SellerProduct
    from .OrdersModel import Orders


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

    reviews:Mapped[list["Review"]] = relationship(uselist=True, back_populates="user")
    
    backet:Mapped[list["SellerProduct"]] = relationship(uselist=True, back_populates="backets", secondary="client_backet_table")

    orders:Mapped[list["Orders"]] = relationship(uselist=True, back_populates="user")
