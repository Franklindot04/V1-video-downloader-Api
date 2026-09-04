from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class VideoOnlyRequest(BaseModel):
    url: str

@router.post("/video-only")
def get_video_only(payload: VideoOnlyRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format_sort": ["res:desc", "fps:desc", "vbr:desc"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        video_formats = [
            f for f in formats
            if f.get("acodec") == "none" and f.get("vcodec") != "none"
        ]

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "video_formats": video_formats,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
