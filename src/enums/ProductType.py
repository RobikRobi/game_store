from pydantic import BaseModel
from src.enums.SubCategoryType import SubCategoryType

class ProductType(BaseModel):
    
    id:int
    name:str
    description:str
    img: str | None
    subCategory:SubCategoryType