from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class EmbedInfoRequest(BaseModel):
    url: str

@router.post("/embed-info")
def get_embed_info(payload: EmbedInfoRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "embed_url": info.get("embed_url"),
            "embed_html": info.get("embed_html"),
            "thumbnail_url": info.get("thumbnail"),
            "title": info.get("title"),
            "author_name": info.get("uploader"),
            "author_url": info.get("uploader_url"),
            "provider_name": info.get("extractor"),
            "provider_url": info.get("webpage_url"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
