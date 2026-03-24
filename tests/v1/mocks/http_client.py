from dataclasses import dataclass, field

from src.apps.common.clients.http_client import BaseHTTPClient


@dataclass
class DummyHTTPClient(BaseHTTPClient):
    EXPECTED_GET_RESPONSES: list = field(default_factory=list)
    EXPECTED_POST_RESPONSES: list = field(default_factory=list)
    LAST_REQUESTS: list[dict] = field(default_factory=list)
    REQUESTS_COUNT: int = 0

    def get(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        self.LAST_REQUESTS.append(
            {
                'url': url,
                'params': params,
                'data': data,
                'headers': headers,
            }
        )
        response = self.EXPECTED_GET_RESPONSES[self.REQUESTS_COUNT]
        self.REQUESTS_COUNT += 1
        return response

    def post(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        self.LAST_REQUESTS.append(
            {
                'url': url,
                'params': params,
                'data': data,
                'headers': headers,
            }
        )
        response = self.EXPECTED_POST_RESPONSES[self.REQUESTS_COUNT]
        self.REQUESTS_COUNT += 1
        return response
