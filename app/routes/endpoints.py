from fastapi import APIRouter, HTTPException
from fastapi.routing import APIRoute

router = APIRouter()

@router.get("/endpoints")
def list_endpoints():
    try:
        from app.main import app

        routes_info = []

        for route in app.routes:
            if isinstance(route, APIRoute):
                routes_info.append({
                    "path": route.path,
                    "name": route.name,
                    "methods": list(route.methods),
                    "summary": route.summary,
                    "endpoint": route.endpoint.__name__,
                    "tags": route.tags,
                })

        return {
            "count": len(routes_info),
            "endpoints": routes_info
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
