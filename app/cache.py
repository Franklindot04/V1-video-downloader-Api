import time
from typing import Any, Optional


_TTL_SECONDS = 30
_CACHE: dict[str, tuple[Any, float]] = {}


def cache_get(key: str) -> Optional[Any]:
    item = _CACHE.get(key)
    if item is None:
        return None
    value, expires_at = item
    if time.time() > expires_at:
        _CACHE.pop(key, None)
        return None
    return value


def cache_set(key: str, value: Any, ttl: int = _TTL_SECONDS) -> None:
    _CACHE[key] = (value, time.time() + ttl)