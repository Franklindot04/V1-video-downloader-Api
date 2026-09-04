from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class DownloadPlanRequest(BaseModel):
    url: str

@router.post("/download-plan")
def download_plan(payload: DownloadPlanRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format_sort": ["res:desc", "fps:desc", "vbr:desc", "abr:desc"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        # Combined formats (progressive)
        combined = [
            f for f in formats
            if f.get("acodec") != "none" and f.get("vcodec") != "none"
        ]

        # Video-only formats
        video_only = [
            f for f in formats
            if f.get("acodec") == "none" and f.get("vcodec") != "none"
        ]

        # Audio-only formats
        audio_only = [
            f for f in formats
            if f.get("vcodec") == "none" and f.get("acodec") != "none"
        ]

        best_combined = combined[0] if combined else None
        best_video = video_only[0] if video_only else None
        best_audio = audio_only[0] if audio_only else None

        smallest = min(formats, key=lambda f: f.get("filesize", float("inf")), default=None)
        largest = max(formats, key=lambda f: f.get("filesize", 0), default=None)

        plan = {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url"),

            "strategy": {
                "recommended": "merge" if best_video and best_audio else "direct",
                "reason": "Best quality requires merging video-only + audio-only"
                if best_video and best_audio else
                "Progressive format available",
            },

            "best_combined": best_combined,
            "best_video_only": best_video,
            "best_audio_only": best_audio,

            "smallest_file": smallest,
            "largest_file": largest,

            "fallbacks": {
                "combined": combined[:5],
                "video_only": video_only[:5],
                "audio_only": audio_only[:5],
            }
        }

        return plan

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
