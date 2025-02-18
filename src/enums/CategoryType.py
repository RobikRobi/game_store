from pydantic import BaseModel

class CategoryType(BaseModel):
    
    id:int
    name:str
    