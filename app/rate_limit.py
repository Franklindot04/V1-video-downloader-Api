import logging
import os

import redis.asyncio as redis
from fastapi import Request
from fastapi.responses import JSONResponse
from redis.exceptions import RedisError
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)

RATE_LIMIT = 60
WINDOW_SECONDS = 60

redis_client = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)

        client = request.client
        client_ip = client.host if client else "unknown"
        key = f"rate_limit:{client_ip}"

        try:
            request_count = await redis_client.incr(key)

            if request_count == 1:
                await redis_client.expire(key, WINDOW_SECONDS)

            if request_count > RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Too many requests. Please slow down."
                    },
                    headers={
                        "Retry-After": str(WINDOW_SECONDS),
                    },
                )
        except RedisError:
            logger.exception("Rate-limit check failed; allowing request")

        return await call_next(request)