from starlette.middleware.gzip import GZipMiddleware


def add_compression(app):
    # Compress responses >= 500 bytes
    app.add_middleware(GZipMiddleware, minimum_size=500)