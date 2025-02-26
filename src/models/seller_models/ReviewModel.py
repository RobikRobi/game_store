import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from src.db import Base

if typing.TYPE_CHECKING:
    from ..product_models.ProductsModel import SellerProduct
    from ..UserModel import User

class Review(Base):
    __tablename__ = "review_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    
    text:Mapped[str]
    
    is_positive:Mapped[bool] = mapped_column(default=True)
    
    seller_product_id:Mapped[int] = mapped_column(ForeignKey("seller_product_table.id", ondelete="CASCADE"))
    product:Mapped["SellerProduct"] = relationship(back_populates="reviews", uselist=False)

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(back_populates="reviews", uselist=False)