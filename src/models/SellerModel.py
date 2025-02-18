import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from src.enums.CurrencyEnum import CurrencyType

from src.db import Base

if typing.TYPE_CHECKING:
    from .ProductsModel import Product
    from .UserModel import User
    


class Review(Base):
    __tablename__ = "review_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    
    text:Mapped[str]
    
    is_positive:Mapped[bool] = mapped_column(default=True)
    
    seller_product_id:Mapped[int] = mapped_column(ForeignKey("seller_product_table.id", ondelete="CASCADE"))
    product:Mapped["SellerProduct"] = relationship(back_populates="reviews", uselist=False)

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(back_populates="reviews", uselist=False)


class SellerProfile(Base):
    __tablename__ = "seller_profile_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    
    shop_name:Mapped[str]
    number:Mapped[str]
    
    is_confirmed:Mapped[bool] = mapped_column(default=False)
    
    user:Mapped["User"] = relationship(back_populates="profile", uselist=False)
    
    products:Mapped[list["SellerProduct"]] = relationship(uselist=True, back_populates="sellerProfile")
    
    
class SellerProduct(Base):
    __tablename__ = "seller_product_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    
    description:Mapped[str]
    price:Mapped[float]
    currency:Mapped[CurrencyType] = mapped_column(default=CurrencyType.RUB)
    selling:Mapped[int] = mapped_column(default=0)
    
    img:Mapped[str]  = mapped_column(nullable=True)

    product_id:Mapped[int] = mapped_column(ForeignKey("product_table.id", ondelete="CASCADE"))
    product:Mapped["Product"] = relationship(back_populates="sellerProducts", uselist=False)
    
    seller_id:Mapped[int] = mapped_column(ForeignKey("seller_profile_table.id", ondelete="CASCADE"))
    sellerProfile:Mapped["SellerProfile"] = relationship(back_populates="products", uselist=False)
    
    reviews:Mapped[list["Review"]] = relationship(uselist=True, back_populates="product")
    
    backets:Mapped[list["User"]] = relationship(uselist=True, back_populates="backet", secondary="client_backet_table")