from pydantic import BaseModel

from src.types.CategoryType import CategoryType
class SubCategoryType(BaseModel):
    
    id:int
    name:str
    
    category:CategoryType