from pydantic import BaseModel
from src.type.SubCategoryType import SubCategoryType

class ProductType(BaseModel):
    
    id:int
    name:str
    description:str
    img: str | None
    subCategory:SubCategoryType