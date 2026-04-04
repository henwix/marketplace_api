from urllib.parse import urlencode
from uuid import uuid4

import pytest
from django.conf import settings
from punq import Container

from src.apps.authentication.constants import SocialAccountProviders
from src.apps.authentication.exceptions.oauth import (
    OAuthInvalidTokenError,
    OAuthProviderEmailNotFoundError,
    OAuthProviderUidNotFoundError,
)
from src.apps.authentication.providers.oauth.google import OAuthGoogleProvider
from src.apps.authentication.services.jwt import BaseJWTService
from tests.v1.mocks.jwt_service import DummyJWTService


@pytest.fixture
def mock_google_provider(mock_container: Container) -> OAuthGoogleProvider:
    mock_container.register(BaseJWTService, DummyJWTService)
    return mock_container.resolve(OAuthGoogleProvider)


def test_get_provider_name_returns_correct_name(mock_google_provider: OAuthGoogleProvider):
    expected_provider_name = SocialAccountProviders.GOOGLE
    assert expected_provider_name == mock_google_provider.provider_name


def test_get_login_url_returns_correct_url(mock_google_provider: OAuthGoogleProvider):
    expected_state = uuid4().hex
    expected_params = {
        'client_id': settings.OAUTH_GOOGLE_CLIENT_ID,
        'scope': 'openid profile email',
        'response_type': 'code',
        'access_type': 'offline',
        'state': expected_state,
        'redirect_uri': settings.OAUTH_GOOGLE_REDIRECT_URI,
    }
    expected_login_url = f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(query=expected_params)}'
    assert expected_login_url == mock_google_provider.get_login_url(state=expected_state)


def test_exchange_code_returns_id_token_and_built_request_is_correct(mock_google_provider: OAuthGoogleProvider):
    expected_code = uuid4().hex
    expected_request = {
        'url': 'https://oauth2.googleapis.com/token',
        'params': None,
        'data': {
            'client_id': settings.OAUTH_GOOGLE_CLIENT_ID,
            'client_secret': settings.OAUTH_GOOGLE_CLIENT_SECRET,
            'code': expected_code,
            'redirect_uri': settings.OAUTH_GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        },
        'headers': None,
    }

    expected_access_token = uuid4().hex
    mock_google_provider.http_client.expected_post_responses = [{'id_token': expected_access_token}]

    access_token = mock_google_provider.exchange_code(code=expected_code)

    assert expected_access_token == access_token
    assert isinstance(access_token, str)
    assert mock_google_provider.http_client.last_requests[0] == expected_request


def test_get_user_data_provider_email_not_found_error_raised_if_no_correct_email(
    mock_google_provider: OAuthGoogleProvider,
):
    expected_token_payload = {
        'sub': '123',
        'given_name': 'Test',
        'family_name': 'Test',
        'name': 'Test Test',
        'picture': 'https://example.com',
    }
    mock_google_provider.jwt_service.EXPECTED_TOKEN_PAYLOAD = expected_token_payload

    with pytest.raises(OAuthProviderEmailNotFoundError):
        mock_google_provider.get_user_data(token='123')


def test_get_user_data_provider_uid_not_found_error_raised_if_no_correct_uid(
    mock_google_provider: OAuthGoogleProvider,
):
    expected_token_payload = {
        'email': 'example@example.com',
        'given_name': 'Test',
        'family_name': 'Test',
        'name': 'Test Test',
        'picture': 'https://example.com',
    }
    mock_google_provider.jwt_service.EXPECTED_TOKEN_PAYLOAD = expected_token_payload

    with pytest.raises(OAuthProviderUidNotFoundError):
        mock_google_provider.get_user_data(token='123')


@pytest.mark.parametrize(
    argnames=['expected_given_name', 'expected_family_name'],
    argvalues=[
        ('Test1', 'Test2'),
        ('    Test1 ', '   Test2  '),
        ('Test1  ', ' Test2'),
        ('Test1', '     Test2'),
    ],
)
def test_get_user_data_returns_correct_data_with_family_and_given_name(
    mock_google_provider: OAuthGoogleProvider,
    expected_given_name: str,
    expected_family_name: str,
):
    expected_email = 'example@example.com'
    expected_picture = 'https://example.com'
    expected_sub = '123'
    expected_token_payload = {
        'email': expected_email,
        'given_name': expected_given_name,
        'sub': expected_sub,
        'family_name': expected_family_name,
        'picture': expected_picture,
    }
    mock_google_provider.jwt_service.EXPECTED_TOKEN_PAYLOAD = expected_token_payload

    user_data = mock_google_provider.get_user_data(token='123')
    assert isinstance(user_data, dict)
    assert expected_given_name.strip() == user_data['first_name']
    assert expected_family_name.strip() == user_data['last_name']
    assert expected_email == user_data['email']
    assert expected_sub == user_data['provider_uid']
    assert expected_picture == user_data['avatar']


@pytest.mark.parametrize(
    argnames='expected_name',
    argvalues=[
        'Test Name',
        'Full Test Name',
        '   Hello  World',
        'Hello World   ',
        '  Hello  World   ',
        '  HelloWorld   ',
        'HelloWorld',
    ],
)
def test_get_user_data_returns_correct_data_with_fullname(
    mock_google_provider: OAuthGoogleProvider,
    expected_name: str,
):
    try:
        first_name, last_name = expected_name.strip().split(sep=' ', maxsplit=1)
    except ValueError:
        first_name = last_name = expected_name

    expected_email = 'example@example.com'
    expected_picture = 'https://example.com'
    expected_sub = '123'
    expected_token_payload = {
        'email': expected_email,
        'name': expected_name,
        'sub': expected_sub,
        'picture': expected_picture,
    }
    mock_google_provider.jwt_service.EXPECTED_TOKEN_PAYLOAD = expected_token_payload

    user_data = mock_google_provider.get_user_data(token='123')
    assert isinstance(user_data, dict)
    assert first_name.strip() == user_data['first_name']
    assert last_name.strip() == user_data['last_name']
    assert expected_email == user_data['email']
    assert expected_sub == user_data['provider_uid']
    assert expected_picture == user_data['avatar']


def test_get_user_data_returns_correct_data_without_any_name(
    mock_google_provider: OAuthGoogleProvider,
):
    expected_email = 'example@example.com'
    expected_picture = 'https://example.com'
    expected_sub = '123'
    expected_token_payload = {
        'email': expected_email,
        'sub': expected_sub,
        'picture': expected_picture,
    }
    mock_google_provider.jwt_service.EXPECTED_TOKEN_PAYLOAD = expected_token_payload

    user_data = mock_google_provider.get_user_data(token='123')
    assert isinstance(user_data, dict)
    assert 'User' == user_data['first_name']
    assert len(user_data['last_name']) == 10
    assert user_data['last_name'].islower()
    assert expected_email == user_data['email']
    assert expected_sub == user_data['provider_uid']
    assert expected_picture == user_data['avatar']


def test_get_user_data_oauth_ivalid_token_error_raised(
    mock_google_provider: OAuthGoogleProvider,
):
    mock_google_provider.jwt_service.RAISE_DECODE_EXCEPTION = True

    with pytest.raises(OAuthInvalidTokenError):
        mock_google_provider.get_user_data(token='123')
