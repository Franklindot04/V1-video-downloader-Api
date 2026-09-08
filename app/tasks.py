import yt_dlp

from app.jobs import update_job


def download_video(job_id, url):
    update_job(job_id, "processing")

    ydl_options = {
        "quiet": True,
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"/tmp/{job_id}.%(ext)s",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=True)

        update_job(
            job_id,
            "completed",
            {"title": info.get("title")},
        )
    except Exception as error:
        update_job(job_id, "failed", {"error": str(error)})
        raise