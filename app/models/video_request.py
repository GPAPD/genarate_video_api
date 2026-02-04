from pydantic import BaseModel
from typing import List, Optional

class VideoRequest(BaseModel):
    product_id: str 
    product_image_count: int 
    product_desc : str   
    template_name : str             
      