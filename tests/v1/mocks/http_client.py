from dataclasses import dataclass, field

from src.apps.common.clients.http_client import BaseHTTPClient


@dataclass
class DummyHTTPClient(BaseHTTPClient):
    expected_get_responses: list = field(default_factory=list)
    expected_post_responses: list = field(default_factory=list)
    last_requests: list[dict] = field(default_factory=list)
    get_requests_count: int = 0
    post_requests_count: int = 0

    def get(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        self.last_requests.append(
            {
                'url': url,
                'params': params,
                'data': data,
                'headers': headers,
            }
        )
        response = self.expected_get_responses[self.get_requests_count]
        self.get_requests_count += 1
        return response

    def post(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        self.last_requests.append(
            {
                'url': url,
                'params': params,
                'data': data,
                'headers': headers,
            }
        )
        response = self.expected_post_responses[self.post_requests_count]
        self.post_requests_count += 1
        return response
