from fastapi import FastAPI
from app.routes.extract import router as extract_router
from app.routes.thumbnail import router as thumbnail_router
from app.routes.system import router as system_router
from app.routes.ping import router as ping_router
from app.routes.info import router as info_router
from app.routes.stats import router as stats_router

app = FastAPI(
    title="V1 Video Downloader API",
    version="1.0.0",
    description="A simple API for extracting video metadata and download links."
)

app.include_router(extract_router)
app.include_router(thumbnail_router)
app.include_router(system_router)
app.include_router(ping_router)
app.include_router(info_router)
app.include_router(stats_router)

@app.get("/")
def root():
    return {"message": "V1 Video Downloader API is running"}
