from punq import Container

from src.apps.authentication.services.oauth.factory import BaseOAuthServiceFactory
from src.apps.authentication.use_cases.oauth.verify import OAuthVerifyUseCase
from tests.v1.authentication.oauth.mocks.service import DummyOAuthService
from tests.v1.authentication.oauth.mocks.service_factory import DummyOAuthServiceFactory


def get_mock_oauth_verify_use_case(
    mock_container: Container,
    state: str = '',
    token: str = '',
    user_data: dict | None = None,
    login_url: str = '',
) -> OAuthVerifyUseCase:
    if user_data is None:
        user_data = {}

    service = DummyOAuthService(
        state=state,
        token=token,
        user_data=user_data,
        login_url=login_url,
    )
    mock_container.register(BaseOAuthServiceFactory, factory=lambda: DummyOAuthServiceFactory(service=service))
    return mock_container.resolve(OAuthVerifyUseCase)
