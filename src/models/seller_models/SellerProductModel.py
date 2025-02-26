import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from src.enum.CurrencyEnum import CurrencyType

from src.db import Base

if typing.TYPE_CHECKING:
    from ..product_models.ProductsModel import Product
    from ..UserModel import User
    from .SellerProfileModel import SellerProfile
    from .ReviewModel import Review
    
    
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