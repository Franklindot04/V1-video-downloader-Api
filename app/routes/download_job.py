import os

import redis
from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from rq import Queue, Retry

from app.jobs import create_job
from app.tasks import download_video


router = APIRouter()


class DownloadJobRequest(BaseModel):
    url: HttpUrl


redis_connection = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)

download_queue = Queue(
    "downloads",
    connection=redis_connection,
)


@router.post("/download-job")
def create_download_job(payload: DownloadJobRequest):
    job_id = create_job()

    download_queue.enqueue(
        download_video,
        job_id,
        str(payload.url),
        retry=Retry(max=3, interval=[10, 30, 60]),
    )

    return {
        "job_id": job_id,
        "status": "queued",
    }