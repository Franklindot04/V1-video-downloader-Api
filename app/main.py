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
from app.routes.playlist_info import router as playlist_info_router
from app.routes.live_status import router as live_status_router
from app.routes.age_rating import router as age_rating_router
from app.routes.embed_info import router as embed_info_router
from app.routes.best_format import router as best_format_router
from app.routes.audio_only import router as audio_only_router
from app.routes.video_only import router as video_only_router
from app.routes.download_url import router as download_url_router
from app.routes.merge_best import router as merge_best_router
from app.routes.format_filter import router as format_filter_router
from app.routes.endpoints import router as endpoints_router
from app.routes.format_summary import router as format_summary_router
from app.routes.download_plan import router as download_plan_router
from app.routes.format_map import router as format_map_router
from app.routes.download_check import router as download_check_router
from app.routes.download_options import router as download_options_router
from app.routes.download_start import router as download_start_router
from app.routes.download_info import router as download_info_router
from app.routes.download_validate import router as download_validate_router
from app.routes.download_flow import router as download_flow_router


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
app.include_router(playlist_info_router)
app.include_router(live_status_router)
app.include_router(age_rating_router)
app.include_router(embed_info_router)
app.include_router(best_format_router)
app.include_router(audio_only_router)
app.include_router(video_only_router)
app.include_router(download_url_router)
app.include_router(merge_best_router)
app.include_router(format_filter_router)
app.include_router(endpoints_router)
app.include_router(format_summary_router)
app.include_router(download_plan_router)
app.include_router(format_map_router)
app.include_router(download_check_router)
app.include_router(download_options_router)
app.include_router(download_start_router)
app.include_router(download_info_router)
app.include_router(download_validate_router)
app.include_router(download_flow_router)


@app.get("/")
def root():
    return {"message": "V1 Video Downloader API is running"}