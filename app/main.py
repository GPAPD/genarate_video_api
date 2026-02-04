from fastapi import FastAPI
from app.api.v1.video import router as video_router


app = FastAPI(
    title="Video Generator API",
    description="API for generating product videos",
    version="1.0.0"
)

# Register routers
app.include_router(video_router, prefix="/api/v1")
