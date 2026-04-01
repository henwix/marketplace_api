from urllib.parse import urlencode
from uuid import uuid4

import pytest
from django.conf import settings
from punq import Container

from src.apps.authentication.constants import SocialAccountProviders
from src.apps.authentication.exceptions.oauth import (
    OAuthIncorrectCodeError,
    OAuthProviderEmailNotFoundError,
    OAuthProviderRequestError,
    OAuthProviderUidNotFoundError,
    OAuthUnverifiedProviderEmailError,
)
from src.apps.authentication.providers.oauth.github import OAuthGitHubProvider


@pytest.fixture
def mock_github_provider(mock_container: Container) -> OAuthGitHubProvider:
    return mock_container.resolve(OAuthGitHubProvider)


def test_get_provider_name_returns_correct_name(mock_github_provider: OAuthGitHubProvider):
    expected_provider_name = SocialAccountProviders.GITHUB
    assert expected_provider_name == mock_github_provider.provider_name


def test_get_login_url_returns_correct_url(mock_github_provider: OAuthGitHubProvider):
    expected_state = uuid4().hex
    expected_params = {
        'client_id': settings.OAUTH_GITHUB_CLIENT_ID,
        'redirect_url': settings.OAUTH_GITHUB_REDIRECT_URI,
        'scope': 'read:user user:email',
        'state': expected_state,
    }
    expected_login_url = f'https://github.com/login/oauth/authorize?{urlencode(query=expected_params)}'
    assert expected_login_url == mock_github_provider.get_login_url(state=expected_state)


def test_exchange_code_returns_access_token_and_built_request_is_correct(mock_github_provider: OAuthGitHubProvider):
    expected_code = uuid4().hex
    expected_request = {
        'url': f'{mock_github_provider._OAUTH_URL}/access_token',
        'params': None,
        'data': {
            'client_id': settings.OAUTH_GITHUB_CLIENT_ID,
            'client_secret': settings.OAUTH_GITHUB_CLIENT_SECRET,
            'code': expected_code,
        },
        'headers': {
            'Accept': 'application/json',
        },
    }

    expected_access_token = uuid4().hex
    mock_github_provider.http_client.expected_post_responses = [{'access_token': expected_access_token}]

    access_token = mock_github_provider.exchange_code(code=expected_code)

    assert expected_access_token == access_token
    assert isinstance(access_token, str)
    assert mock_github_provider.http_client.last_requests[0] == expected_request


def test_exchange_code_incorrect_code_error_raised(mock_github_provider: OAuthGitHubProvider):
    mock_github_provider.http_client.expected_post_responses = [{'error': 'bad_verification_code'}]
    with pytest.raises(OAuthIncorrectCodeError):
        mock_github_provider.exchange_code(code=uuid4().hex)


def test_exchange_code_unverified_user_email_error_raised(mock_github_provider: OAuthGitHubProvider):
    mock_github_provider.http_client.expected_post_responses = [{'error': 'unverified_user_email'}]
    with pytest.raises(OAuthUnverifiedProviderEmailError):
        mock_github_provider.exchange_code(code=uuid4().hex)


def test_exchange_code_provider_request_error_raised_if_incorrect_client_credentials(
    mock_github_provider: OAuthGitHubProvider,
):
    mock_github_provider.http_client.expected_post_responses = [{'error': 'incorrect_client_credentials'}]
    with pytest.raises(OAuthProviderRequestError):
        mock_github_provider.exchange_code(code=uuid4().hex)


def test_exchange_code_provider_request_error_raised_if_redirect_uri_mismatch(
    mock_github_provider: OAuthGitHubProvider,
):
    mock_github_provider.http_client.expected_post_responses = [{'error': 'redirect_uri_mismatch'}]
    with pytest.raises(OAuthProviderRequestError):
        mock_github_provider.exchange_code(code=uuid4().hex)


def test_exchange_code_provider_request_error_raised_if_no_error_and_access_token(
    mock_github_provider: OAuthGitHubProvider,
):
    mock_github_provider.http_client.expected_post_responses = [{}]
    with pytest.raises(OAuthProviderRequestError):
        mock_github_provider.exchange_code(code=uuid4().hex)


@pytest.mark.parametrize(
    argnames=['expected_name', 'expected_email', 'expected_id', 'expected_avatar_url'],
    argvalues=[
        ('Test Name', 'test@example.com', '123456789', 'https://example.avatar.com'),
        ('Nametest', 'name@example.com', '987654321', 'https://avatars.com/avatar.jpg'),
        ('Hello World', 'helloworld@example.com', '111222333', 'https://images.test.com/helloworld.png'),
        ('test', 'testtest@example.com', '81265871265', 'https://images.test.com/hajsfjahf1.png'),
        ('test    name', 'testtest@example.com', '81925725', 'https://images.test.com/hajsfjahf1.png'),
        ('   test    name', 'testtest@example.com', '81925725', 'https://images.test.com/hajsfjahf1.png'),
        ('   test    name  ', 'testtest@example.com', '81925725', 'https://images.test.com/hajsfjahf1.png'),
    ],
)
def test_get_user_data_returns_correct_data_with_name_field(
    mock_github_provider: OAuthGitHubProvider,
    expected_name: str,
    expected_email: str,
    expected_id: str,
    expected_avatar_url: str,
):
    try:
        expected_first_name, expected_last_name = expected_name.strip().split(' ', 1)
    except ValueError:
        expected_first_name = expected_name
        expected_last_name = expected_name

    expected_token = uuid4().hex
    expected_request = {
        'url': mock_github_provider._USER_API_URL,
        'params': None,
        'data': None,
        'headers': {
            'Authorization': f'Bearer {expected_token}',
        },
    }
    mock_github_provider.http_client.expected_get_responses = [
        {
            'name': expected_name,
            'email': expected_email,
            'id': expected_id,
            'avatar_url': expected_avatar_url,
        }
    ]

    user_data = mock_github_provider.get_user_data(token=expected_token)

    assert user_data.get('first_name') == expected_first_name.strip()
    assert user_data.get('last_name') == expected_last_name.strip()
    assert user_data.get('email') == expected_email
    assert user_data.get('provider_uid') == expected_id
    assert user_data.get('avatar') == expected_avatar_url
    assert mock_github_provider.http_client.last_requests[0] == expected_request


@pytest.mark.parametrize('expected_login', ['test', '  test', 'test   ', '  test   '])
def test_get_user_data_returns_correct_data_with_login_field(
    mock_github_provider: OAuthGitHubProvider,
    expected_login: str,
):
    expected_email = 'test@example.com'
    expected_token = uuid4().hex
    expected_id = '123412341234'
    expected_avatar_url = 'https://example.com'

    expected_request = {
        'url': mock_github_provider._USER_API_URL,
        'params': None,
        'data': None,
        'headers': {
            'Authorization': f'Bearer {expected_token}',
        },
    }
    mock_github_provider.http_client.expected_get_responses = [
        {
            'name': None,
            'login': expected_login,
            'email': expected_email,
            'id': expected_id,
            'avatar_url': expected_avatar_url,
        }
    ]

    user_data = mock_github_provider.get_user_data(token=expected_token)

    assert user_data.get('first_name') == expected_login.strip()
    assert user_data.get('last_name') == expected_login.strip()
    assert user_data.get('email') == expected_email
    assert user_data.get('provider_uid') == expected_id
    assert user_data.get('avatar') == expected_avatar_url
    assert mock_github_provider.http_client.last_requests[0] == expected_request


def test_get_user_data_returns_correct_data_with_extra_request_with_primary_email(
    mock_github_provider: OAuthGitHubProvider,
):
    expected_login = 'testlogin'
    expected_email = 'test@example.com'
    expected_token = uuid4().hex
    expected_id = '123412341234'
    expected_avatar_url = 'https://example.com'

    expected_first_request = {
        'url': mock_github_provider._USER_API_URL,
        'params': None,
        'data': None,
        'headers': {
            'Authorization': f'Bearer {expected_token}',
        },
    }
    expected_second_request = {
        'url': f'{mock_github_provider._USER_API_URL}/emails',
        'params': None,
        'data': None,
        'headers': {
            'Authorization': f'Bearer {expected_token}',
        },
    }
    mock_github_provider.http_client.expected_get_responses = [
        {
            'name': None,
            'login': expected_login,
            'email': None,
            'id': expected_id,
            'avatar_url': expected_avatar_url,
        },
        [
            {
                'email': expected_email,
                'verified': True,
                'primary': True,
                'visibility': 'private',
            },
            {
                'email': 'hgashfsg@example.com',
                'verified': True,
                'primary': False,
                'visibility': 'private',
            },
        ],
    ]

    user_data = mock_github_provider.get_user_data(token=expected_token)

    assert user_data.get('first_name') == expected_login
    assert user_data.get('last_name') == expected_login
    assert user_data.get('email') == expected_email
    assert user_data.get('provider_uid') == expected_id
    assert user_data.get('avatar') == expected_avatar_url
    assert mock_github_provider.http_client.last_requests[0] == expected_first_request
    assert mock_github_provider.http_client.last_requests[1] == expected_second_request


@pytest.mark.parametrize(
    argnames='expected_second_get_response',
    argvalues=[[{'email': '123@example.com', 'verified': True, 'primary': False, 'visibility': 'private'}], []],
)
def test_get_user_data_provider_email_not_found_error_raised_if_not_correct_email(
    mock_github_provider: OAuthGitHubProvider,
    expected_second_get_response: dict | list,
):
    expected_login = 'testlogin'
    expected_token = uuid4().hex
    expected_id = '123412341234'
    expected_avatar_url = 'https://example.com'

    expected_first_request = {
        'url': mock_github_provider._USER_API_URL,
        'params': None,
        'data': None,
        'headers': {
            'Authorization': f'Bearer {expected_token}',
        },
    }
    expected_second_request = {
        'url': f'{mock_github_provider._USER_API_URL}/emails',
        'params': None,
        'data': None,
        'headers': {
            'Authorization': f'Bearer {expected_token}',
        },
    }
    mock_github_provider.http_client.expected_get_responses = [
        {
            'name': None,
            'login': expected_login,
            'email': None,
            'id': expected_id,
            'avatar_url': expected_avatar_url,
        },
        expected_second_get_response,
    ]

    with pytest.raises(OAuthProviderEmailNotFoundError):
        mock_github_provider.get_user_data(token=expected_token)

    assert mock_github_provider.http_client.last_requests[0] == expected_first_request
    assert mock_github_provider.http_client.last_requests[1] == expected_second_request


def test_get_user_data_uid_not_found_error_raised_if_no_provider_id(
    mock_github_provider: OAuthGitHubProvider,
):
    expected_login = 'testlogin'
    expected_email = 'test@example.com'
    expected_token = uuid4().hex
    expected_avatar_url = 'https://example.com'

    expected_first_request = {
        'url': mock_github_provider._USER_API_URL,
        'params': None,
        'data': None,
        'headers': {
            'Authorization': f'Bearer {expected_token}',
        },
    }
    mock_github_provider.http_client.expected_get_responses = [
        {
            'name': None,
            'login': expected_login,
            'email': expected_email,
            'id': None,
            'avatar_url': expected_avatar_url,
        }
    ]

    with pytest.raises(OAuthProviderUidNotFoundError):
        mock_github_provider.get_user_data(token=expected_token)

    assert mock_github_provider.http_client.last_requests[0] == expected_first_request
