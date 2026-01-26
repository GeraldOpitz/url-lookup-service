from fastapi import HTTPException
import logging
from app.db import get_connection

logger = logging.getLogger(__name__)

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

    logger.info("Checking URL safety: %s", normalized_url)

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM malicious_urls WHERE url = %s",
                    (normalized_url,),
                )
                result = cur.fetchone()
    except Exception as exc:
        logger.error(
            "Database unavailable, cannot evaluate URL",
            exc_info=exc,
        )
        raise HTTPException(
            status_code=503,
            detail="URL lookup service temporarily unavailable",
        )

    if result:
        logger.info("URL marked as malicious: %s", normalized_url)
        return {
            "url": normalized_url,
            "safe": False,
            "reason": "URL found in malware database",
        }

    logger.info("URL marked as safe: %s", normalized_url)
    return {
        "url": normalized_url,
        "safe": True,
    }
