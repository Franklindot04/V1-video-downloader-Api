from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class PlaylistInfoRequest(BaseModel):
    url: str

@router.post("/playlist-info")
def get_playlist_info(payload: PlaylistInfoRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": True,  # important for playlist metadata
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "description": info.get("description"),
            "entries": info.get("entries"),
            "playlist_count": info.get("playlist_count"),
            "thumbnails": info.get("thumbnails"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
