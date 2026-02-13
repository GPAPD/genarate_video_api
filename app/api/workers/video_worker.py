import time
from app.services.video_service import generate_video

def generate_video_job(payload):

    print("Generating video...")
    time.sleep(10)

    # call your moviepy video creation here
    generate_video(payload)

    return "completed"