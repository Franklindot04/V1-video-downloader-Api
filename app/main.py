from fastapi import FastAPI
from app.routes.extract import router as extract_router
from app.routes.thumbnail import router as thumbnail_router
from app.routes.system import router as system_router
from app.routes.ping import router as ping_router
from app.routes.info import router as info_router
from app.routes.stats import router as stats_router
from app.routes.player import router as player_router
from app.routes.formats import router as formats_router
from app.routes.uploader import router as uploader_router
from app.routes.duration import router as duration_router
from app.routes.title import router as title_router
from app.routes.description import router as description_router
from app.routes.thumbnail_info import router as thumbnail_info_router
from app.routes.keywords import router as keywords_router
from app.routes.captions import router as captions_router
from app.routes.chapters import router as chapters_router


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
app.include_router(player_router)
app.include_router(formats_router)
app.include_router(uploader_router)
app.include_router(duration_router)
app.include_router(title_router)
app.include_router(description_router)
app.include_router(thumbnail_info_router)
app.include_router(keywords_router)
app.include_router(captions_router)
app.include_router(chapters_router)


@app.get("/")
def root():
    return {"message": "V1 Video Downloader API is running"}