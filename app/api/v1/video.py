from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models.video_request import VideoRequest
from app.models.video_response import VideoResponse
from app.services.video_service import generate_video

router = APIRouter(prefix="/video",tags=["Video"])

@router.post("/generate", response_model=VideoResponse, summary="Generate a product video")

def generate_video_endpoint( request: VideoRequest, background_tasks: BackgroundTasks ):

    """
    Starts video generation in the background
    """
    
    try:
        background_tasks.add_task(generate_video, request)

        return VideoResponse( status="started",message="Video generation started successfully")

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

