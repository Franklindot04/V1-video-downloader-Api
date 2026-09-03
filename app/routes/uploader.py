from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class UploaderRequest(BaseModel):
    url: str

@router.post("/uploader")
def get_uploader(payload: UploaderRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "uploader": info.get("uploader"),
            "uploader_id": info.get("uploader_id"),
            "uploader_url": info.get("uploader_url"),
            "channel_id": info.get("channel_id"),
            "channel_url": info.get("channel_url"),
            "channel_follower_count": info.get("channel_follower_count"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
