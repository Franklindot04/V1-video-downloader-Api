from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp
from datetime import datetime

router = APIRouter()

class DownloadManifestRequest(BaseModel):
    url: str
    format_id: str | None = None

@router.post("/download-manifest")
def download_manifest(payload: DownloadManifestRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format_sort": ["res:desc", "fps:desc", "vbr:desc", "abr:desc"],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        if not formats:
            raise HTTPException(status_code=404, detail="No formats available")

        # Select format
        selected = None
        if payload.format_id:
            selected = next((f for f in formats if f.get("format_id") == payload.format_id), None)

        if not selected:
            selected = next(
                (f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"),
                None
            )

        if not selected:
            raise HTTPException(status_code=404, detail="No progressive format available")

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

        warnings = []
        errors = []

        if info.get("is_live"):
            warnings.append("Video is live; formats may be incomplete")

        if info.get("age_limit") and info.get("age_limit") >= 18:
            warnings.append("Video is age-restricted")

        if info.get("availability") == "unavailable":
            errors.append("Video is unavailable")

        if not selected.get("url"):
            errors.append("Selected format has no download URL")

        # Execution plan
        steps = []

        steps.append("Validate URL")
        steps.append("Extract metadata")
        steps.append("Select format")
        steps.append("Check safety conditions")

        if strategy == "direct":
            steps.append("Download combined file directly")
        elif strategy == "merge":
            steps.append("Download video-only stream")
            steps.append("Download audio-only stream")
            steps.append("Merge using ffmpeg")
        else:
            steps.append("Fallback: choose another format")

        ffmpeg_cmd = None
        if strategy == "merge":
            ffmpeg_cmd = (
                "ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a copy output.mp4"
            )

        manifest = {
            "manifest_version": "1.0",
            "generated_at": datetime.utcnow().isoformat(),
            "generator": "V1-video-downloader-API",

            "metadata": {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "webpage_url": info.get("webpage_url"),
                "uploader": info.get("uploader"),
                "thumbnails": info.get("thumbnails", [])[:3],
                "description": (info.get("description") or "")[:300],
            },

            "format": {
                "format_id": selected.get("format_id"),
                "type": type_,
                "strategy": strategy,
                "container": selected.get("container"),
                "vcodec": selected.get("vcodec"),
                "acodec": selected.get("acodec"),
                "resolution": selected.get("resolution"),
                "fps": selected.get("fps"),
                "bitrate": selected.get("tbr"),
                "filesize": selected.get("filesize"),
                "fragment_count": len(selected.get("fragments", [])),
                "download_url": selected.get("url"),
            },

            "execution_plan": steps,
            "ffmpeg_recommendation": ffmpeg_cmd,

            "warnings": warnings,
            "errors": errors,
            "safe_to_proceed": len(errors) == 0,
        }

        return manifest

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
