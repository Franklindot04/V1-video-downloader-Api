from fastapi import APIRouter

router = APIRouter()

@router.get("/ping", tags=["System"])
def ping():
    return {"message": "pong"}
