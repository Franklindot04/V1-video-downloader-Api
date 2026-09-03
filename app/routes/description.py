from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class DescriptionRequest(BaseModel):
    url: str

@router.post("/description")
def get_description(payload: DescriptionRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "description": info.get("description")
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
