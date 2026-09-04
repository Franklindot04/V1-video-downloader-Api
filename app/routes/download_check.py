from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class DownloadCheckRequest(BaseModel):
    url: str

@router.post("/download-check")
def download_check(payload: DownloadCheckRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        progressive = [
            f for f in formats
            if f.get("acodec") != "none" and f.get("vcodec") != "none"
        ]

        video_only = [
            f for f in formats
            if f.get("acodec") == "none" and f.get("vcodec") != "none"
        ]

        audio_only = [
            f for f in formats
            if f.get("vcodec") == "none" and f.get("acodec") != "none"
        ]

        downloadable = len(formats) > 0

        warnings = []

        if info.get("is_live"):
            warnings.append("Video is live; formats may be unavailable.")

        if info.get("age_limit") and info.get("age_limit") >= 18:
            warnings.append("Video is age-restricted.")

        if info.get("availability") == "unavailable":
            warnings.append("Video is unavailable.")

        if not progressive and (video_only and audio_only):
            strategy = "merge"
            reason = "Best quality requires merging video-only + audio-only."
        elif progressive:
            strategy = "direct"
            reason = "Progressive formats available."
        else:
            strategy = "fallback"
            reason = "Limited formats available."

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url"),

            "downloadable": downloadable,
            "warnings": warnings,

            "formats": {
                "progressive_count": len(progressive),
                "video_only_count": len(video_only),
                "audio_only_count": len(audio_only),
                "total_formats": len(formats),
            },

            "strategy": {
                "recommended": strategy,
                "reason": reason,
            },

            "fallbacks": {
                "progressive": progressive[:3],
                "video_only": video_only[:3],
                "audio_only": audio_only[:3],
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
