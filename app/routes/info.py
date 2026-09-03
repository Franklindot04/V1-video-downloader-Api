from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class InfoRequest(BaseModel):
    url: str

@router.post("/info")
def get_info(payload: InfoRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "uploader": info.get("uploader"),
            "upload_date": info.get("upload_date"),
            "description": info.get("description"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
