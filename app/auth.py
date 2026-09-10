import os

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response


API_KEY = os.getenv("API_KEY")


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if not API_KEY:
            return await call_next(request)

        path = request.url.path
        if path in ("/docs", "/openapi.json", "/health", "/ping"):
            return await call_next(request)

        key = request.headers.get("X-API-Key")
        if key != API_KEY:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API key"},
            )

        return await call_next(request)