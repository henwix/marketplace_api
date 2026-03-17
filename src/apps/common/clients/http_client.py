from abc import ABC, abstractmethod

import requests

from src.apps.common.exceptions.http_client import HTTPClientError


class BaseHTTPClient(ABC):
    @abstractmethod
    def get(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict: ...

    @abstractmethod
    def post(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict: ...


class HTTPClient(BaseHTTPClient):
    def _request(
        self,
        method: str,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        try:
            response = requests.request(method=method, url=url, params=params, data=data, headers=headers)
            response.raise_for_status()
        except requests.RequestException as error:
            exc_response = getattr(error, 'response', None)
            raise HTTPClientError(
                method=method,
                url=url,
                response_status=exc_response.status_code if exc_response is not None else None,
                error_details=str(error),
            ) from error
        return response.json()

    def get(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        return self._request(method='get', url=url, params=params, data=data, headers=headers)

    def post(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        return self._request(method='post', url=url, params=params, data=data, headers=headers)
