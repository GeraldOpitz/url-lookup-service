from fastapi import FastAPI, Request

app = FastAPI(title="URL Lookup Service")

@app.get("/urlinfo/1/{hostname_and_port}/{path:path}")
def url_info(hostname_and_port: str, path: str, request: Request):
    query_string = request.url.query
    full_path = path

    if query_string:
        full_path = f"{path}?{query_string}"

    return {
        "hostname_and_port": hostname_and_port,
        "path": full_path
    }
