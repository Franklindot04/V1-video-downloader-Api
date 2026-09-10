import os

import redis.asyncio as redis
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


class AbuseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip abuse checks for docs/health/ping to keep DX smooth
        path = request.url.path
        if path in ("/docs", "/openapi.json", "/health", "/ping"):
            return await call_next(request)

        ip = request.client.host
        if not ip:
            return await call_next(request)

        key = f"abuse:{ip}"

        count = await redis_client.incr(key)
        if count == 1:
            # First request for this IP in this window
            await redis_client.expire(key, 60)

        if count > 200:
            return JSONResponse(
                status_code=429,
                content={"detail": "Suspicious activity detected"},
            )

        return await call_next(request)