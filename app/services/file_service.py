import os
import shutil
from fastapi import HTTPException
from app.models.video_response import VideoResponse

UPLOAD_DIR = "uploads"
def save_file(fileb) :
            # Validate CSV
        if not fileb.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files allowed")

        file_path = os.path.join(UPLOAD_DIR, fileb.filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(fileb.file, buffer)
        
        return VideoResponse( 
               status_code=200,     
               respones=file_path, 
               message="file save successfully"
               )
             