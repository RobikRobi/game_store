from enum import Enum

class OrderStatus(Enum):
    
    CREATED = "CREATED"
    
    PAYED = "PAYED"
    
    FINISHED = "FINISHED"