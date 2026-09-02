def generate_download_urls(formats):
    """
    Extract direct download URLs from yt-dlp formats.
    Returns a simplified list containing only what the frontend needs.
    """
    results = []

    for f in formats:
        results.append({
            "format_id": f.get("format_id"),
            "ext": f.get("ext"),
            "resolution": f.get("resolution"),
            "filesize": f.get("filesize"),
            "url": f.get("url"),  # direct download link
        })

    return results
