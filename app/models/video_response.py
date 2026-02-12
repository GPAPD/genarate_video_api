from pydantic import BaseModel

class VideoResponse(BaseModel):
    status_code: int
    respones: object  
    message: str 
