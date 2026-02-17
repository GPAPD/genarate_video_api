from fastapi import APIRouter, BackgroundTasks, HTTPException, File, Form, UploadFile
from typing import Annotated


from app.models.video_request import VideoRequest
from app.models.video_response import VideoResponse
from app.services.video_service import generate_video
from app.services.file_service import save_file , read_csv_and_generate_video
from app.services.upload_videos_service import upload_videos_cloudinary

router = APIRouter(prefix="/video",tags=["Video"])

@router.post("/generate", response_model=VideoResponse, summary="Generate a product video")
def generate_video_endpoint(request: VideoRequest, background_tasks: BackgroundTasks ):
   
    try:
        # background_tasks.add_task(generate_video, request)
        video_id = generate_video(request.model_dump())
        upload_videos_cloudinary(f"./gen_videos/{video_id}.mp4",video_id)
        return VideoResponse(status_code=200, respones="", message="Video generation started successfully")

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.post("/upload_csv",summary="uplad csv file")
def upload_csv(fileb: Annotated[UploadFile, File()],):

    try:
       response = save_file(fileb)
       return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}"
        )

@router.post("generate_all", summary="Generate product videos using csv file ")
def generate_videos_using_csv():
    try :
        response = read_csv_and_generate_video()
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}"
        )

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

