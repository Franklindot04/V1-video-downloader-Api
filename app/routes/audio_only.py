from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class AudioOnlyRequest(BaseModel):
    url: str

@router.post("/audio-only")
def get_audio_only(payload: AudioOnlyRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format_sort": ["abr:desc", "asr:desc"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        audio_formats = [
            f for f in formats
            if f.get("vcodec") == "none" and f.get("acodec") != "none"
        ]

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "audio_formats": audio_formats,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
