
import typing
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from src.types.currencyType import CurrencyType

from src.db import Base

if typing.TYPE_CHECKING:
    from ..products.products_models import Product
    from ..seller.seller_models import SellerProduct
    from ..app_auth.auth_models import User
    

class ClientBacket(Base):
    __tablename__ = "client_backet_table"

    counts:Mapped[int] = mapped_column(default=1)
    
    product_id:Mapped[int] = mapped_column(ForeignKey("seller_product_table.id", ondelete="CASCADE"),primary_key=True)
    product:Mapped["SellerProduct"] = relationship(uselist=False)
    
    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"),primary_key=True)
    user:Mapped["User"] = relationship(uselist=False)