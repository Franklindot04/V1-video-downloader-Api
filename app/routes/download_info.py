from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class DownloadInfoRequest(BaseModel):
    url: str
    format_id: str

@router.post("/download-info")
def download_info(payload: DownloadInfoRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])
        selected = next((f for f in formats if f.get("format_id") == payload.format_id), None)

        if not selected:
            raise HTTPException(status_code=404, detail="Format ID not found")

        # Determine type
        if selected.get("vcodec") != "none" and selected.get("acodec") != "none":
            type_ = "combined"
            strategy = "direct"
        elif selected.get("vcodec") != "none":
            type_ = "video_only"
            strategy = "merge"
        elif selected.get("acodec") != "none":
            type_ = "audio_only"
            strategy = "merge"
        else:
            type_ = "unknown"
            strategy = "fallback"

        # ffmpeg recommendation (string only)
        ffmpeg_cmd = None
        if strategy == "merge":
            ffmpeg_cmd = (
                "ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a copy output.mp4"
            )

        warnings = []
        if info.get("is_live"):
            warnings.append("Video is live; formats may be incomplete.")
        if info.get("age_limit") and info.get("age_limit") >= 18:
            warnings.append("Video is age-restricted.")
        if info.get("availability") == "unavailable":
            warnings.append("Video is unavailable.")

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url"),

            "format_id": selected.get("format_id"),
            "type": type_,
            "strategy": strategy,

            "technical": {
                "container": selected.get("container"),
                "vcodec": selected.get("vcodec"),
                "acodec": selected.get("acodec"),
                "bitrate": selected.get("tbr"),
                "resolution": selected.get("resolution"),
                "fps": selected.get("fps"),
                "filesize": selected.get("filesize"),
                "fragment_count": len(selected.get("fragments", [])),
                "has_fragments": bool(selected.get("fragments")),
            },

            "download_url": selected.get("url"),
            "ffmpeg_recommendation": ffmpeg_cmd,
            "warnings": warnings,
            "safe_to_download": selected.get("url") is not None,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
