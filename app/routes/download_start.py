from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class DownloadStartRequest(BaseModel):
    url: str
    format_id: str | None = None

@router.post("/download-start")
def download_start(payload: DownloadStartRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format_sort": ["res:desc", "fps:desc", "vbr:desc", "abr:desc"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        if not formats:
            raise HTTPException(status_code=404, detail="No formats available for download")

        # If user specifies a format_id
        selected = None
        if payload.format_id:
            selected = next((f for f in formats if f.get("format_id") == payload.format_id), None)
            if not selected:
                raise HTTPException(status_code=404, detail="Format ID not found")

        # If no format_id, pick best combined
        if not selected:
            selected = next(
                (f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"),
                None
            )

        if not selected:
            raise HTTPException(status_code=404, detail="No progressive format available")

        # Determine type
        if selected.get("vcodec") != "none" and selected.get("acodec") != "none":
            type_ = "combined"
            strategy = "direct"
        elif selected.get("vcodec") != "none":
            type_ = "video_only"
            strategy = "merge"
        elif selected.get("acodec") != "none":
            type_ = "audio_only"
            strategy = "merge"
        else:
            type_ = "unknown"
            strategy = "fallback"

        warnings = []

        if info.get("is_live"):
            warnings.append("Video is live; formats may be incomplete.")

        if info.get("age_limit") and info.get("age_limit") >= 18:
            warnings.append("Video is age-restricted.")

        if info.get("availability") == "unavailable":
            warnings.append("Video is unavailable.")

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url"),

            "format_id": selected.get("format_id"),
            "type": type_,
            "strategy": strategy,
            "download_url": selected.get("url"),

            "warnings": warnings,
            "safe_to_download": selected.get("url") is not None,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
