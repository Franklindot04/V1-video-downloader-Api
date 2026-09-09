from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html


router = APIRouter()


@router.get("/docs", include_in_schema=False)
def custom_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="V1 Video Downloader API — Documentation",
        swagger_favicon_url=(
            "https://fastapi.tiangolo.com/img/favicon.png"
        ),
    )