import os
import shutil
from fastapi import HTTPException
import pandas as pd
from rq import Retry

from app.models.video_response import VideoResponse
from app.api.workers.video_worker import generate_video_job
from app.connection.queue_conn import video_queue
from app.models.video_request import VideoRequest

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
             

def read_csv_and_generate_video():

    df = pd.read_csv("./uploads/videogen.csv",dtype=str)

    job_ids = []

    for _, row in df.iterrows():

        request = VideoRequest(
            product_id=row["id"],
            product_desc=row["ShortDesc"],
            product_image_count=row["ViewIndex"],
            product_price=row["Retail"],
            product_sale_price=row["PromoPrice"],
            template=row["template"]
        )

        # Convert to dict for Redis serialization safety
        job = video_queue.enqueue(
            generate_video_job,
            request.model_dump()   # important
        )

        job_ids.append(job.id)

    return VideoResponse(
        status_code=200,
        respones=job_ids,   # return all jobs
        message="Successfully started video generation"
    )