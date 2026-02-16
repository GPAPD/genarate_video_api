import os
import cloudinary
import cloudinary.uploader

def upload_videos_cloudinary(video_url : str, public_id : str):
    try :
        #Cloudinery credentials 
        cloudinary.config( 
        cloud_name = os.getenv("SS_CLOUD_NAME"), 
        api_key = os.getenv("SS_API_KEY"), 
        api_secret = os.getenv("SS_SECRET")
        )

        result = cloudinary.uploader.upload(
            video_url,
            public_id = f"{os.getenv('SAVE_PATH')}{public_id}",
            resource_type="video"
        )
        return result
    except Exception as e:
        return f"Cloudinery file upload failed: {str(e)}"
