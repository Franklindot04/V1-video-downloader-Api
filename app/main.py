from fastapi import FastAPI
from app.routes.extract import router as extract_router

app = FastAPI(
    title="V1 Video Downloader API",
    version="1.0.0",
    description="A simple API for extracting video metadata and download links."
)

app.include_router(extract_router)

@app.get("/")
def root():
    return {"message": "V1 Video Downloader API is running"}
