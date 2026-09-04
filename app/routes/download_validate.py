from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class DownloadValidateRequest(BaseModel):
    url: str
    format_id: str

@router.post("/download-validate")
def download_validate(payload: DownloadValidateRequest):
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
            return {
                "valid": False,
                "errors": ["Format ID not found"],
                "warnings": [],
                "recommended": "choose_another_format",
            }

        errors = []
        warnings = []

        # Basic checks
        if not selected.get("url"):
            errors.append("Format has no direct download URL")

        if selected.get("vcodec") == "none" and selected.get("acodec") == "none":
            errors.append("Format has no audio or video codec")

        if selected.get("container") is None:
            warnings.append("Container is missing")

        if selected.get("resolution") is None and selected.get("vcodec") != "none":
            warnings.append("Resolution is missing")

        if selected.get("tbr") is None:
            warnings.append("Bitrate is missing")

        # Live / restricted / unavailable
        if info.get("is_live"):
            warnings.append("Video is live; formats may be incomplete")

        if info.get("age_limit") and info.get("age_limit") >= 18:
            warnings.append("Video is age-restricted")

        if info.get("availability") == "unavailable":
            errors.append("Video is unavailable")

        # Determine type + strategy
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

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "recommended": (
                "proceed" if len(errors) == 0 else "choose_another_format"
            ),

            "format": {
                "format_id": selected.get("format_id"),
                "type": type_,
                "strategy": strategy,
                "container": selected.get("container"),
                "vcodec": selected.get("vcodec"),
                "acodec": selected.get("acodec"),
                "resolution": selected.get("resolution"),
                "bitrate": selected.get("tbr"),
                "fps": selected.get("fps"),
                "filesize": selected.get("filesize"),
            },

            "download_url": selected.get("url"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
