import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from src.db import Base

if typing.TYPE_CHECKING:
    from .CategoryModel import Category

class SubCategory(Base):
    __tablename__ = "subcategory_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)    
    name:Mapped[str]
    
    category_id:Mapped[int] = mapped_column(ForeignKey("category_table.id", ondelete="CASCADE"))
    
    category:Mapped["Category"] = relationship(back_populates="subCategories", uselist=False)
    