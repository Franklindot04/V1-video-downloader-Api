from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class CaptionsRequest(BaseModel):
    url: str

@router.post("/captions")
def get_captions(payload: CaptionsRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "subtitles": info.get("subtitles"),
            "automatic_captions": info.get("automatic_captions"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
