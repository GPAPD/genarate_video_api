from pydantic import BaseModel

class VideoResponse(BaseModel):
    status: str  
    message: str 
