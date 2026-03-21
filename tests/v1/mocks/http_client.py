from src.apps.common.clients.http_client import BaseHTTPClient


class DummyHTTPClient(BaseHTTPClient):
    def get(
        self, url: str, params: dict | None = None, data: dict | None = None, headers: dict | None = None
    ) -> dict: ...

    def post(
        self, url: str, params: dict | None = None, data: dict | None = None, headers: dict | None = None
    ) -> dict: ...
