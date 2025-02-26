import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from src.db import Base

if typing.TYPE_CHECKING:
    from .SubcategoryModel import SubCategory

class Category(Base):
    __tablename__ = "category_table"
    
    id:Mapped[int] = mapped_column(primary_key=True)    
    name:Mapped[str]
    
    subCategories:Mapped[list["SubCategory"]] = relationship(uselist=True, back_populates="category")
    