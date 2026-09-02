from fastapi import FastAPI

app = FastAPI(
    title="V1 Video Downloader API",
    version="1.0.0",
    description="A simple API for extracting video metadata and download links."
)

@app.get("/")
def root():
    return {"message": "V1 Video Downloader API is running"}
