from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_safe_url():
    """A URL not present in the malicious list should be marked as safe."""
    response = client.get("/urlinfo/1/www.google.com/search")
    assert response.status_code == 200

    data = response.json()
    assert data["safe"] is True
    assert data["url"] == "www.google.com/search"


def test_malicious_url():
    """A URL present in the malicious list should be flagged as unsafe."""
    response = client.get("/urlinfo/1/www.bad.com/malware")
    assert response.status_code == 200

    data = response.json()
    assert data["safe"] is False
    assert data["url"] == "www.bad.com/malware"
    assert "reason" in data


def test_malicious_url_with_http_scheme():
    """URLs with http:// scheme should be normalized before lookup."""
    response = client.get("/urlinfo/1/http://www.bad.com/malware")
    assert response.status_code == 200

    data = response.json()
    assert data["safe"] is False
    assert data["url"] == "www.bad.com/malware"


def test_malicious_url_with_https_scheme():
    """URLs with https:// scheme should be normalized before lookup."""
    response = client.get("/urlinfo/1/https://www.bad.com/malware")
    assert response.status_code == 200

    data = response.json()
    assert data["safe"] is False
    assert data["url"] == "www.bad.com/malware"
