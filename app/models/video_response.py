from pydantic import BaseModel
from typing import Any

class VideoResponse(BaseModel):
    status_code: int
    respones: Any  
    message: str 
