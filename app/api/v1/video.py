from fastapi import APIRouter, BackgroundTasks, HTTPException, File, Form, UploadFile
from typing import Annotated


from app.models.video_request import VideoRequest
from app.models.video_response import VideoResponse
from app.services.video_service import generate_video
from app.services.file_service import save_file

router = APIRouter(prefix="/video",tags=["Video"])

@router.post("/generate", response_model=VideoResponse, summary="Generate a product video")
def generate_video_endpoint(request: VideoRequest, background_tasks: BackgroundTasks ):
   
    try:
        # background_tasks.add_task(generate_video, request)
        generate_video(request)
        return VideoResponse(status_code=200, respones="", message="Video generation started successfully")

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.post("/generate-all",summary="Generate product videos using csv file")
def genarate_videos_using_csv(fileb: Annotated[UploadFile, File()],):

    try:
       respond = save_file(fileb)
       return respond

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


# @router.get(
#         "/{product_id}",
#           response_model=VideoResponse, 
#           summary="Get video by id"
#           )
# def get_video(product_id: str):
#     return VideoResponse(
#         status="completed",
#         message=f"Video {product_id} fetched"
#     )

