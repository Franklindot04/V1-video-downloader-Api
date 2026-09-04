from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class FormatFilterRequest(BaseModel):
    url: str
    resolution: str | None = None
    ext: str | None = None
    vcodec: str | None = None
    acodec: str | None = None
    container: str | None = None

@router.post("/format-filter")
def format_filter(payload: FormatFilterRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        def matches(f):
            if payload.resolution and payload.resolution not in f.get("resolution", ""):
                return False
            if payload.ext and payload.ext != f.get("ext"):
                return False
            if payload.vcodec and payload.vcodec not in f.get("vcodec", ""):
                return False
            if payload.acodec and payload.acodec not in f.get("acodec", ""):
                return False
            if payload.container and payload.container != f.get("container"):
                return False
            return True

        filtered = [f for f in formats if matches(f)]

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "filtered_formats": filtered,
            "filter_count": len(filtered),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
