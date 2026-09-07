from fastapi import APIRouter, HTTPException

from app.jobs import get_job


router = APIRouter()


@router.get("/job/{job_id}")
def job_status(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job