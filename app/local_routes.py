import os

from fastapi import FastAPI


def register_local_worker_routes(app: FastAPI):
    if os.getenv("ENABLE_LOCAL_WORKER_ROUTES") != "true":
        return

    from app.routes.download_job import router as download_job_router
    from app.routes.download_result import router as download_result_router
    from app.routes.job_status import router as job_status_router

    app.include_router(download_job_router)
    app.include_router(job_status_router)
    app.include_router(download_result_router)