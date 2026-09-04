from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class ChaptersRequest(BaseModel):
    url: str

@router.post("/chapters")
def get_chapters(payload: ChaptersRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "chapters": info.get("chapters")
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
