from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class FakeCursor:
    def __init__(self, result):
        self.result = result

    def execute(self, query, params):
        pass

    def fetchone(self):
        return self.result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


class FakeConnection:
    def __init__(self, result):
        self.result = result

    def cursor(self):
        return FakeCursor(self.result)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

def test_safe_url(monkeypatch):
    """URL not present in DB should be marked as safe."""

    def fake_get_connection():
        return FakeConnection(None)

    monkeypatch.setattr("app.service.get_connection", fake_get_connection)

    response = client.get("/urlinfo/1/www.google.com/search")
    assert response.status_code == 200
    assert response.json()["safe"] is True


def test_malicious_url(monkeypatch):
    """URL present in DB should be marked as malicious."""

    def fake_get_connection():
        return FakeConnection((1,))

    monkeypatch.setattr("app.service.get_connection", fake_get_connection)

    response = client.get("/urlinfo/1/www.bad.com/malware")
    data = response.json()

    assert data["safe"] is False
    assert data["url"] == "www.bad.com/malware"
    assert "reason" in data


def test_fallback_when_db_is_down(monkeypatch):
    """Service should fall back when DB is unavailable."""
    
    def fake_get_connection():
        raise Exception("DB unavailable")

    monkeypatch.setattr("app.service.get_connection", fake_get_connection)

    response = client.get("/urlinfo/1/www.anything.com/test")
    assert response.status_code == 503
    assert response.json()["detail"] == "URL lookup service temporarily unavailable"


def test_url_normalization(monkeypatch):
    """URLs with scheme should be normalized."""

    def fake_get_connection():
        return FakeConnection((1,))

    monkeypatch.setattr("app.service.get_connection", fake_get_connection)

    response = client.get("/urlinfo/1/https://www.bad.com/malware")
    data = response.json()

    assert data["safe"] is False
    assert data["url"] == "www.bad.com/malware"
