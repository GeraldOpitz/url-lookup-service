from fastapi import FastAPI
from app.service import check_url_safety

app = FastAPI(title="URL Lookup Service")

@app.get("/urlinfo/1/{hostname_and_port}/{path:path}")
def url_info(hostname_and_port: str, path: str):
    return check_url_safety(hostname_and_port, path)
