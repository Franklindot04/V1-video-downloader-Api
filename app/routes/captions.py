from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class CaptionsRequest(BaseModel):
    url: str

@router.post(
    "/captions",
    tags=["Captions"],
    summary="Get available caption tracks",
    description=(
        "Returns manual subtitle tracks and automatic captions "
        "when they are available for a supported video URL."
    ),
    responses={
        200: {
            "description": "Caption metadata",
            "content": {
                "application/json": {
                    "example": {
                        "subtitles": {
                            "en": [
                                {
                                    "ext": "vtt",
                                    "url": (
                                        "https://example.com/"
                                        "subtitles/en.vtt"
                                    ),
                                }
                            ]
                        },
                        "automatic_captions": {
                            "en": [
                                {
                                    "ext": "vtt",
                                    "url": (
                                        "https://example.com/"
                                        "captions/en.vtt"
                                    ),
                                }
                            ]
                        },
                    }
                }
            },
        }
    },
)
def get_captions(payload: CaptionsRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "subtitles": info.get("subtitles"),
            "automatic_captions": info.get("automatic_captions"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
