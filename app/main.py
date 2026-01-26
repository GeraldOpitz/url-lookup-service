from fastapi import FastAPI
import os
import logging
from contextlib import asynccontextmanager

from app.logging_config import setup_logging
from app.service import check_url_safety

setup_logging()

logger = logging.getLogger("url-lookup-service")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Application lifespan handler.

    Logs public service information at startup and performs
    cleanup actions during shutdown.
    """
    host = os.getenv("PUBLIC_HOST", "localhost")
    port = os.getenv("PUBLIC_PORT", "8000")

    logger.info(f"Swagger UI available at http://{host}:{port}/docs")

    yield

    logger.info("Application shutdown complete.")


app = FastAPI(
    title="URL Lookup Service",
    description=(
        "A simple HTTP service that determines whether a given URL is considered malicious. "
        "It is intended to be queried by an HTTP proxy before allowing outbound connections."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get(
    "/urlinfo/1/{hostname_and_port}/{path:path}",
    summary="Check URL safety",
    description=(
        "Checks whether the given URL is considered malicious.\n\n"
        "The URL is provided as two components:\n"
        "- `hostname_and_port`: the hostname (and optional port)\n"
        "- `path`: the original path and query string\n\n"
        "The service responds indicating whether the URL is safe to access."
    ),
)
def url_info(hostname_and_port: str, path: str):
    """
    Returns information about whether a URL is safe or malicious.

    The service normalizes URLs that include http:// or https://
    before checking them against the internal malware database.
    """
    return check_url_safety(hostname_and_port, path)
