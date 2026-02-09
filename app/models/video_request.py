from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional

class VideoRequest(BaseModel):
    product_id: str 
    product_image_count: int 
    product_price: str
    product_sale_price:str
    product_desc : str   
    template : int  = 1           
