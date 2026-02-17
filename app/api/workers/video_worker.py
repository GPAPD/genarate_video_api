import time
from app.services.video_service import generate_video,delete_jpg_files
from app.services.upload_videos_service import upload_videos_cloudinary

def generate_video_job(payload):

    print("Generating video...")
    time.sleep(5)

    # call your moviepy video creation here
    product_id = generate_video(payload)

    #upload to the cloudinery 
    upload_to_cloudinary = upload_videos_cloudinary(f"./gen_videos/{product_id}.mp4",product_id)

    time.sleep(3)
    #delete after upload
    delete_jpg_files(f"./gen_videos/{product_id}.mp4")

    return "completed"