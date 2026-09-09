from pathlib import Path

import yt_dlp

from app.cleanup import cleanup_old_files
from app.jobs import update_job
from app.storage import (
    DOWNLOAD_DIR,
    MAX_STORAGE_BYTES,
    ensure_download_directory,
    get_storage_usage_bytes,
    has_storage_capacity,
)


def download_video(job_id, url):
    cleanup_old_files()
    ensure_download_directory()

    if not has_storage_capacity():
        update_job(
            job_id,
            "failed",
            {
                "error": (
                    "Local storage quota has been reached. "
                    f"Maximum allowed storage is {MAX_STORAGE_BYTES} bytes."
                )
            },
        )
        return

    update_job(job_id, "processing")

    output_template = str(DOWNLOAD_DIR / f"{job_id}.%(ext)s")

    ydl_options = {
        "quiet": True,
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output_template,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=True)

        downloaded_file = Path(
            ydl.prepare_filename(info)
        )

        if not downloaded_file.exists():
            raise FileNotFoundError(
                "Download completed but the expected output file was not found."
            )

        if not has_storage_capacity(downloaded_file.stat().st_size):
            downloaded_file.unlink(missing_ok=True)
            raise RuntimeError(
                "Download would exceed the local 500 MB storage quota."
            )

        update_job(
            job_id,
            "completed",
            {
                "title": info.get("title"),
                "filename": downloaded_file.name,
                "storage_bytes": get_storage_usage_bytes(),
            },
        )
    except Exception as error:
        update_job(job_id, "failed", {"error": str(error)})
        raise