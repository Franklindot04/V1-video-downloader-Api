from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class FormatSummaryRequest(BaseModel):
    url: str

@router.post("/format-summary")
def format_summary(payload: FormatSummaryRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        resolutions = sorted(
            {f.get("resolution") for f in formats if f.get("resolution")},
            reverse=True
        )

        video_codecs = sorted(
            {f.get("vcodec") for f in formats if f.get("vcodec") and f.get("vcodec") != "none"}
        )

        audio_codecs = sorted(
            {f.get("acodec") for f in formats if f.get("acodec") and f.get("acodec") != "none"}
        )

        containers = sorted(
            {f.get("container") for f in formats if f.get("container")}
        )

        progressive = [
            f for f in formats
            if f.get("acodec") != "none" and f.get("vcodec") != "none"
        ]

        dash_video = [
            f for f in formats
            if f.get("acodec") == "none" and f.get("vcodec") != "none"
        ]

        dash_audio = [
            f for f in formats
            if f.get("vcodec") == "none" and f.get("acodec") != "none"
        ]

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),

            "summary": {
                "resolution_options": resolutions,
                "video_codecs": video_codecs,
                "audio_codecs": audio_codecs,
                "containers": containers,
                "progressive_count": len(progressive),
                "dash_video_count": len(dash_video),
                "dash_audio_count": len(dash_audio),
            },

            "recommended": {
                "mobile": next((f for f in progressive if "360" in f.get("resolution", "")), None),
                "desktop": next((f for f in progressive if "720" in f.get("resolution", "")), None),
                "high_quality": next((f for f in progressive if "1080" in f.get("resolution", "")), None),
                "audio_only": next((f for f in dash_audio), None),
                "video_only": next((f for f in dash_video), None),
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
