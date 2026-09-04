from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class KeywordsRequest(BaseModel):
    url: str

@router.post("/keywords")
def get_keywords(payload: KeywordsRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "tags": info.get("tags"),
            "categories": info.get("categories"),
            "keywords": info.get("keywords"),  # yt-dlp sometimes provides this
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
