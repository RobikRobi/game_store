from pydantic import BaseModel

from src.type.CategoryType import CategoryType
class SubCategoryType(BaseModel):
    
    id:int
    name:str
    
    category:CategoryType