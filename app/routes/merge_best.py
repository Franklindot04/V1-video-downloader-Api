from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class MergeBestRequest(BaseModel):
    url: str

@router.post("/merge-best")
def merge_best(payload: MergeBestRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format_sort": ["res:desc", "fps:desc", "vbr:desc", "abr:desc"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        # Best video-only
        best_video = next(
            (f for f in formats if f.get("acodec") == "none" and f.get("vcodec") != "none"),
            None
        )

        # Best audio-only
        best_audio = next(
            (f for f in formats if f.get("vcodec") == "none" and f.get("acodec") != "none"),
            None
        )

        if not best_video or not best_audio:
            raise HTTPException(status_code=404, detail="Could not find both audio and video streams")

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "best_video": best_video,
            "best_audio": best_audio,
            "video_url": best_video.get("url"),
            "audio_url": best_audio.get("url"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
