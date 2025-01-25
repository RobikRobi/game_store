
import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from src.db import Base

if typing.TYPE_CHECKING:
    from src.seller.seller_models import SellerProduct
    
class Category(Base):
    __tablename__ = "category_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)    
    name:Mapped[str]
    
    subCategories:Mapped[list["SubCategory"]] = relationship(uselist=True, back_populates="category")
    
class SubCategory(Base):
    __tablename__ = "subcategory_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)    
    name:Mapped[str]
    
    category_id:Mapped[int] = mapped_column(ForeignKey("category_table.id", ondelete="CASCADE"))
    
    category:Mapped["Category"] = relationship(back_populates="subCategories", uselist=False)
    


class Product(Base):
    __tablename__ = "product_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)    
    name:Mapped[str]
    description:Mapped[str]
    
    img:Mapped[str]  = mapped_column(nullable=True)
    
    subCategory_id:Mapped[int] = mapped_column(ForeignKey("subcategory_table.id", ondelete="CASCADE"))
    subCategory:Mapped["SubCategory"] = relationship( uselist=False)
    
    
    sellerProducts:Mapped[list["SellerProduct"]] = relationship(uselist=True, back_populates="product")