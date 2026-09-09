import shutil
from pathlib import Path


DOWNLOAD_DIR = Path("downloads")
MAX_STORAGE_BYTES = 500 * 1024 * 1024


def ensure_download_directory():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_storage_usage_bytes():
    ensure_download_directory()

    return sum(
        path.stat().st_size
        for path in DOWNLOAD_DIR.iterdir()
        if path.is_file()
    )


def has_storage_capacity(required_bytes=0):
    return get_storage_usage_bytes() + required_bytes <= MAX_STORAGE_BYTES


def get_free_storage_bytes():
    usage = shutil.disk_usage(DOWNLOAD_DIR)

    return usage.free