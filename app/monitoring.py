from time import perf_counter

from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware


REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API request latency in seconds",
    ["method", "endpoint"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)

        start_time = perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            endpoint = request.scope.get("route")
            path = getattr(endpoint, "path", request.url.path)
            elapsed = perf_counter() - start_time

            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=path,
                status=str(status_code),
            ).inc()

            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=path,
            ).observe(elapsed)