import pytest
from punq import Container

from src.apps.authentication.commands.oauth import OAuthVerifyCommand
from src.apps.authentication.exceptions.social_account import SocialAccountProviderAlreadyConnectedError
from src.apps.authentication.models.social_account import SocialAccount
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError, UserWithEmailAlreadyExistsError
from src.apps.users.models import User
from tests.v1.authentication.oauth.factories import SocialAccountModelFactory
from tests.v1.authentication.oauth.use_cases.conftest import get_mock_oauth_verify_use_case
from tests.v1.users.factories import UserModelFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames=[
        'expected_provider_name',
        'expected_first_name',
        'expected_last_name',
        'expected_email',
        'expected_provider_uid',
        'expected_avatar',
    ],
    argvalues=[
        ('test_provider', 'Test', 'Name', 'test@example.com', '123123123', 'https://test.avatar.com'),
        ('github', 'Git', 'Hub', 'github@example.com', '5823823', 'https://github.avatar.com'),
        ('google', 'Google', 'Test', 'google@example.com', '88422141', 'https://google.avatar.com'),
        ('twitter', 'Twitter', 'Name', 'twitter@example.com', '125482175', 'https://twitter.avatar.com'),
    ],
)
def test_oauth_verify_creates_new_user_and_returns_tokens_if_social_account_does_not_exist_and_user_not_authorized(
    mock_container: Container,
    expected_provider_name: str,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_provider_uid: str,
    expected_avatar: str,
):
    use_case = get_mock_oauth_verify_use_case(
        mock_container=mock_container,
        user_data={
            'first_name': expected_first_name,
            'last_name': expected_last_name,
            'email': expected_email,
            'provider_uid': expected_provider_uid,
            'avatar': expected_avatar,
        },
    )

    assert User.objects.count() == 0
    assert SocialAccount.objects.count() == 0

    command = OAuthVerifyCommand(
        user_id=None,
        code='1',
        state='1',
        provider=expected_provider_name,
    )
    tokens = use_case.execute(command=command)

    assert isinstance(tokens, dict)
    assert 'access' in tokens
    assert 'refresh' in tokens
    assert User.objects.count() == 1
    assert SocialAccount.objects.count() == 1
    assert User.objects.filter(
        first_name=expected_first_name,
        last_name=expected_last_name,
        email=expected_email,
        avatar=expected_avatar,
    ).exists()
    assert SocialAccount.objects.filter(
        provider=expected_provider_name,
        user__first_name=expected_first_name,
        user__last_name=expected_last_name,
        user__email=expected_email,
        user__avatar=expected_avatar,
    ).exists()


@pytest.mark.django_db
def test_oauth_verify_new_social_account_created_if_does_not_exists_and_user_authorized(
    mock_container: Container,
    user: User,
):
    expected_result = {'detail': 'Provider successfully connected to your account'}
    use_case = get_mock_oauth_verify_use_case(mock_container=mock_container)
    command = OAuthVerifyCommand(user_id=user.pk, code='1', state='1', provider='test_provider')

    assert not SocialAccount.objects.filter(user=user, provider='test_provider').exists()

    result = use_case.execute(command=command)

    assert expected_result == result
    assert SocialAccount.objects.filter(user=user, provider='test_provider').exists()


@pytest.mark.django_db
def test_oauth_verify_provider_already_connected_error_raised_if_provider_already_connected_and_user_authorized(
    mock_container: Container,
):
    expected_provider_uid = '123123123'
    expected_provider_name = 'test_provider'

    social_account = SocialAccountModelFactory.create(
        provider=expected_provider_name, provider_uid=expected_provider_uid
    )

    use_case = get_mock_oauth_verify_use_case(
        mock_container=mock_container,
        user_data={
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'test@example.com',
            'provider_uid': expected_provider_uid,
            'avatar': 'https://avatar.example.com',
        },
    )
    command = OAuthVerifyCommand(user_id=social_account.user.pk, code='1', state='1', provider=expected_provider_name)

    with pytest.raises(SocialAccountProviderAlreadyConnectedError):
        use_case.execute(command=command)


@pytest.mark.django_db
def test_oauth_verify_provider_already_connected_error_raised_if_same_provider_already_connected_to_current_user(
    mock_container: Container,
    social_account: SocialAccount,
):
    use_case = get_mock_oauth_verify_use_case(
        mock_container=mock_container,
        user_data={
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'test@example.com',
            'provider_uid': '123412344',
            'avatar': 'https://avatar.example.com',
        },
    )
    command = OAuthVerifyCommand(
        user_id=social_account.user.pk,
        code='1',
        state='1',
        provider=social_account.provider,
    )
    with pytest.raises(SocialAccountProviderAlreadyConnectedError):
        use_case.execute(command=command)


@pytest.mark.django_db
def test_oauth_verify_returns_tokens_if_provider_already_connected_and_user_not_authorized(
    mock_container: Container,
):
    expected_provider_uid = '123123123'
    expected_provider_name = 'test_provider'
    SocialAccountModelFactory.create(provider=expected_provider_name, provider_uid=expected_provider_uid)

    use_case = get_mock_oauth_verify_use_case(
        mock_container=mock_container,
        user_data={
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'test@example.com',
            'provider_uid': expected_provider_uid,
            'avatar': 'https://avatar.example.com',
        },
    )
    command = OAuthVerifyCommand(user_id=None, code='1', state='1', provider=expected_provider_name)
    tokens = use_case.execute(command=command)

    assert isinstance(tokens, dict)
    assert 'access' in tokens
    assert 'refresh' in tokens
    assert User.objects.count() == 1
    assert SocialAccount.objects.count() == 1


@pytest.mark.django_db
def test_oauth_verify_user_not_created_and_user_with_email_already_exists_error_raised(
    mock_container: Container,
):
    expected_email = 'test@example.com'
    UserModelFactory.create(email=expected_email)

    use_case = get_mock_oauth_verify_use_case(
        mock_container=mock_container,
        user_data={
            'first_name': 'First',
            'last_name': 'Last',
            'email': expected_email,
            'provider_uid': '123123123',
            'avatar': 'https://avatar.example.com',
        },
    )
    command = OAuthVerifyCommand(user_id=None, code='1', state='1', provider='test_provider')
    with pytest.raises(UserWithEmailAlreadyExistsError):
        use_case.execute(command=command)


@pytest.mark.django_db
def test_oauth_verify_user_not_found_error_raised_if_user_authorized(mock_container: Container):
    use_case = get_mock_oauth_verify_use_case(mock_container=mock_container)
    command = OAuthVerifyCommand(user_id=1, code='1', state='1', provider='test_provider')
    with pytest.raises(UserNotFoundError):
        use_case.execute(command=command)


@pytest.mark.django_db
def test_oauth_verify_user_not_active_error_raised_if_user_authorized(mock_container: Container):
    user = UserModelFactory.create(is_active=False)
    use_case = get_mock_oauth_verify_use_case(mock_container=mock_container)
    command = OAuthVerifyCommand(user_id=user.pk, code='1', state='1', provider='test_provider')
    with pytest.raises(UserNotActiveError):
        use_case.execute(command=command)


@pytest.mark.django_db
def test_oauth_verify_user_not_active_error_raised_if_user_not_authorized_and_social_account_exists(
    mock_container: Container,
):
    user = UserModelFactory.create(is_active=False)
    social_account: SocialAccountModelFactory = SocialAccountModelFactory.create(user=user)
    use_case = get_mock_oauth_verify_use_case(
        mock_container=mock_container,
        user_data={
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'test@example.com',
            'provider_uid': social_account.provider_uid,
            'avatar': 'https://avatar.example.com',
        },
    )
    command = OAuthVerifyCommand(user_id=None, code='1', state='1', provider=social_account.provider)
    with pytest.raises(UserNotActiveError):
        use_case.execute(command=command)
