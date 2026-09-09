from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.jobs import get_job
from app.storage import DOWNLOAD_DIR


router = APIRouter()


@router.get("/download-result/{job_id}")
def download_result(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail="Job is not completed yet.",
        )

    filename = job.get("data", {}).get("filename")

    if not filename:
        raise HTTPException(
            status_code=404,
            detail="Download file metadata not found.",
        )

    file_path = (DOWNLOAD_DIR / filename).resolve()
    download_directory = DOWNLOAD_DIR.resolve()

    if download_directory not in file_path.parents:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream",
    )