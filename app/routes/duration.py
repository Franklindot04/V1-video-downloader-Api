from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class DurationRequest(BaseModel):
    url: str

def format_duration(seconds: int | None):
    if seconds is None:
        return None
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

@router.post("/duration")
def get_duration(payload: DurationRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        duration_seconds = info.get("duration")
        duration_formatted = format_duration(duration_seconds)

        return {
            "duration_seconds": duration_seconds,
            "duration_formatted": duration_formatted,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
