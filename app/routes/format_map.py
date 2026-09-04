from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp
from collections import defaultdict

router = APIRouter()

class FormatMapRequest(BaseModel):
    url: str

@router.post("/format-map")
def format_map(payload: FormatMapRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        formats = info.get("formats", [])

        map_res = defaultdict(list)
        map_container = defaultdict(list)
        map_vcodec = defaultdict(list)
        map_acodec = defaultdict(list)
        map_type = defaultdict(list)
        map_fps = defaultdict(list)
        map_bitrate = defaultdict(list)

        for f in formats:
            res = f.get("resolution") or "unknown"
            container = f.get("container") or "unknown"
            vcodec = f.get("vcodec") or "none"
            acodec = f.get("acodec") or "none"
            fps = f.get("fps") or 0
            bitrate = f.get("tbr") or 0

            # Resolution grouping
            map_res[res].append(f)

            # Container grouping
            map_container[container].append(f)

            # Codec grouping
            map_vcodec[vcodec].append(f)
            map_acodec[acodec].append(f)

            # Type grouping
            if vcodec != "none" and acodec != "none":
                map_type["progressive"].append(f)
            elif vcodec != "none":
                map_type["video_only"].append(f)
            elif acodec != "none":
                map_type["audio_only"].append(f)
            else:
                map_type["unknown"].append(f)

            # FPS grouping
            if fps >= 60:
                map_fps["60+"].append(f)
            elif fps >= 30:
                map_fps["30-59"].append(f)
            else:
                map_fps["0-29"].append(f)

            # Bitrate grouping
            if bitrate >= 5000:
                map_bitrate["high"].append(f)
            elif bitrate >= 1500:
                map_bitrate["medium"].append(f)
            else:
                map_bitrate["low"].append(f)

        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "webpage_url": info.get("webpage_url"),

            "map": {
                "resolution": dict(map_res),
                "container": dict(map_container),
                "video_codec": dict(map_vcodec),
                "audio_codec": dict(map_acodec),
                "type": dict(map_type),
                "fps": dict(map_fps),
                "bitrate": dict(map_bitrate),
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
