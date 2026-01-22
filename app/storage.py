from pathlib import Path

BAD_URLS_FILE = Path("bad_urls.txt")

def load_bad_urls() -> set[str]:
    if not BAD_URLS_FILE.exists():
        return set()
    
    with BAD_URLS_FILE.open("r", encoding="utf-8") as f:
        bad_urls = {line.strip() for line in f if line.strip()}

    return bad_urls

MALICIOUS_URLS = load_bad_urls()
