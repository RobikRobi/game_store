from pydantic import BaseModel

from src.enums.CategoryType import CategoryType
class SubCategoryType(BaseModel):
    
    id:int
    name:str
    
    category:CategoryType