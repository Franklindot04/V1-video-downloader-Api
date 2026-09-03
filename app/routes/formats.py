from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class FormatsRequest(BaseModel):
    url: str

@router.post("/formats")
def get_formats(payload: FormatsRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "formats": info.get("formats", [])
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
