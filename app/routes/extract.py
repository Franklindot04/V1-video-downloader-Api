from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

from app.services.format_filter import filter_formats

router = APIRouter()

class ExtractRequest(BaseModel):
    url: str
    kind: str | None = None        # "audio", "video", or None
    resolution: str | None = None  # e.g. "720p"

@router.post("/extract")
def extract_video_info(payload: ExtractRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = [
            {
                "format_id": f.get("format_id"),
                "ext": f.get("ext"),
                "resolution": f.get("resolution"),
                "filesize": f.get("filesize"),
                "url": f.get("url"),
                "vcodec": f.get("vcodec"),
                "acodec": f.get("acodec"),
            }
            for f in info.get("formats", [])
        ]

        kind = payload.kind if hasattr(payload, "kind") else None
        resolution = payload.resolution if hasattr(payload, "resolution") else None

        filtered = filter_formats(formats, kind=kind, resolution=resolution)

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "formats": filtered,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
