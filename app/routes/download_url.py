from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class DownloadURLRequest(BaseModel):
    url: str
    format_id: str | None = None

@router.post("/download-url")
def get_download_url(payload: DownloadURLRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        # If user specifies a format_id, return that exact one
        if payload.format_id:
            match = next((f for f in formats if f.get("format_id") == payload.format_id), None)
            if not match:
                raise HTTPException(status_code=404, detail="Format ID not found")
            return {
                "title": info.get("title"),
                "format_id": payload.format_id,
                "download_url": match.get("url"),
            }

        # Otherwise return the default best combined format
        best = next(
            (f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"),
            None
        )

        if not best:
            raise HTTPException(status_code=404, detail="No combined format available")

        return {
            "title": info.get("title"),
            "format_id": best.get("format_id"),
            "download_url": best.get("url"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
