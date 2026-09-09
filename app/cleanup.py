import time

from app.storage import DOWNLOAD_DIR, ensure_download_directory


MAX_AGE_SECONDS = 86400


def cleanup_old_files():
    ensure_download_directory()
    cutoff = time.time() - MAX_AGE_SECONDS

    for path in DOWNLOAD_DIR.iterdir():
        if path.is_file() and path.stat().st_mtime < cutoff:
            path.unlink()