from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class BestFormatRequest(BaseModel):
    url: str

@router.post("/best-format")
def get_best_format(payload: BestFormatRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format_sort": ["res:desc", "fps:desc", "vbr:desc", "abr:desc"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        best_video_audio = next(
            (f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"),
            None
        )

        best_video_only = next(
            (f for f in formats if f.get("acodec") == "none"),
            None
        )

        best_audio_only = next(
            (f for f in formats if f.get("vcodec") == "none"),
            None
        )

        return {
            "best_video_audio": best_video_audio,
            "best_video_only": best_video_only,
            "best_audio_only": best_audio_only,
            "title": info.get("title"),
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
