from app.storage import MALICIOUS_URLS

def normalize_url(url: str) -> str:
    if url.startswith("http://"):
        return url[len("http://"):]
    if url.startswith("https://"):
        return url[len("https://"):]
    return url

def build_full_url(hostname_and_port: str, path: str) -> str:
    if path:
        return f"{hostname_and_port}/{path}".rstrip("/")
    return hostname_and_port

def check_url_safety(hostname_and_port: str, path: str) -> dict:
    full_url = build_full_url(hostname_and_port, path)
    normalized_url = normalize_url(full_url)

    if normalized_url in MALICIOUS_URLS:
        return {
            "url": normalized_url,
            "safe": False,
            "reason": "URL found in malware database"
        }

    return {
        "url": normalized_url,
        "safe": True
    }
