import json
import os
from uuid import uuid4

import redis


JOB_TTL_SECONDS = 86400

redis_client = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
)


def create_job():
    job_id = str(uuid4())
    redis_client.setex(
        f"job:{job_id}",
        JOB_TTL_SECONDS,
        json.dumps({"status": "queued"}),
    )
    return job_id


def update_job(job_id, status, data=None):
    payload = {"status": status}

    if data is not None:
        payload["data"] = data

    redis_client.setex(
        f"job:{job_id}",
        JOB_TTL_SECONDS,
        json.dumps(payload),
    )


def get_job(job_id):
    raw_job = redis_client.get(f"job:{job_id}")

    if raw_job is None:
        return None

    return json.loads(raw_job)