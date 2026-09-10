import os
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    # Ensure yt-dlp cache directory exists
    os.makedirs("/tmp/yt-cache", exist_ok=True)
    yield