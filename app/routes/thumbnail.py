from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class ThumbnailRequest(BaseModel):
    url: str

@router.post("/thumbnail")
def get_thumbnail(payload: ThumbnailRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "thumbnail": info.get("thumbnail")
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
