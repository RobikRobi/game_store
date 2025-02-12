from pydantic import BaseModel
from types.CurrencyEnum import CurrencyType

class CreateSellerProfile(BaseModel):
    
    shop_name:str
    number:str
    
class CreateProduct(BaseModel):
    
    description:str
    price:float
    currency:CurrencyType
    product_id:int