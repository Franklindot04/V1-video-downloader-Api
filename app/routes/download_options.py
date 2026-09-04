from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class DownloadOptionsRequest(BaseModel):
    url: str

@router.post("/download-options")
def download_options(payload: DownloadOptionsRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format_sort": ["res:desc", "fps:desc", "vbr:desc", "abr:desc"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        options = []

        for f in formats:
            resolution = f.get("resolution") or "audio"
            label = resolution if resolution != "audio" else "Audio Only"

            options.append({
                "label": label,
                "format_id": f.get("format_id"),
                "container": f.get("container"),
                "vcodec": f.get("vcodec"),
                "acodec": f.get("acodec"),
                "filesize": f.get("filesize"),
                "download_url": f.get("url"),
                "type": (
                    "combined" if f.get("vcodec") != "none" and f.get("acodec") != "none"
                    else "video_only" if f.get("vcodec") != "none"
                    else "audio_only"
                ),
                "recommended": resolution in ["720p", "1080p", "audio"],
            })

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url"),
            "options": options,
            "count": len(options),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
