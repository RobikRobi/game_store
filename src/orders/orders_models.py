import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column,relationship

from src.db import Base
from types.OrderStatusEnum import OrderStatus

if typing.TYPE_CHECKING:
    from src.app_auth.auth_models import User
    from src.seller.seller_models import SellerProduct

class OrdersSellerProduct(Base):
    __tablename__ = "orders_seller_product_table"
    
    counts:Mapped[int] = mapped_column(default=0)
    
    seller_product_id:Mapped[int] = mapped_column(ForeignKey("seller_product_table.id", ondelete="CASCADE"), primary_key=True)
    seller_product:Mapped["SellerProduct"] = relationship(uselist=False)
    
    order_id:Mapped[int] = mapped_column(ForeignKey("orders_table.id", ondelete="CASCADE"), primary_key=True)
    

class Orders(Base):
    __tablename__ = "orders_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)
    
    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(back_populates="orders", uselist=False)
    
    seller_products:Mapped[list["SellerProduct"]] = relationship(uselist=True,
                                                                       secondary="orders_seller_product_table"
                                                                       )
    
    price:Mapped[float]
    
    orderStatus:Mapped[OrderStatus]