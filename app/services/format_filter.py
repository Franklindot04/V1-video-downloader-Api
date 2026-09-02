def filter_formats(formats, kind: str | None = None, resolution: str | None = None):
    results = formats

    if kind == "audio":
        results = [f for f in results if f.get("vcodec") == "none"]
    elif kind == "video":
        results = [f for f in results if f.get("acodec") != "none"]

    if resolution:
        results = [f for f in results if f.get("resolution") == resolution]

    return results
