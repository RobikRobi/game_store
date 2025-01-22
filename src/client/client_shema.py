from pydantic import BaseModel

class CreateReview(BaseModel):
    text:str
    is_positive:bool
    seller_product_id:int