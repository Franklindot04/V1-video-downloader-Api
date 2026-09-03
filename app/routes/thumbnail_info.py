from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class ThumbnailInfoRequest(BaseModel):
    url: str

@router.post("/thumbnail-info")
def get_thumbnail_info(payload: ThumbnailInfoRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "thumbnail": info.get("thumbnail"),
            "thumbnail_id": info.get("thumbnail_id"),
            "thumbnails": info.get("thumbnails"),  # yt-dlp sometimes returns multiple
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
