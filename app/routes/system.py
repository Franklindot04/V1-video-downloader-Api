from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["System"])
def health():
    return {"status": "ok"}

@router.get("/version", tags=["System"])
def version():
    return {"version": "1.0.0"}
