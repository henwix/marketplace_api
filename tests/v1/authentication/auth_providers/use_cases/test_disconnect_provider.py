import pytest
from punq import Container

from src.apps.authentication.commands.auth_providers import DisconnectAuthProviderCommand
from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.authentication.exceptions.auth_providers import (
    AuthProviderNotConnectedError,
    AuthProviderNotSupportedError,
    AuthProvidersNotConnectedError,
    UnableToDisconnectAuthProviderError,
)
from src.apps.authentication.models.auth_provider import AuthProvider
from src.apps.authentication.use_cases.auth_providers.disconnect_provider import DisconnectAuthProviderUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.authentication.auth_providers.factories import AuthProviderModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def disconnect_auth_provider_use_case(container: Container) -> DisconnectAuthProviderUseCase:
    return container.resolve(DisconnectAuthProviderUseCase)


@pytest.mark.django_db
def test_disconnect_auth_provider_returns_none_if_successfully_disconnected_with_usable_password_and_two_providers(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
    user: User,
):
    AuthProviderModelFactory.create(user=user, provider='github')
    provider_two = AuthProviderModelFactory.create(user=user, provider='google')
    command = DisconnectAuthProviderCommand(user_id=user.pk, provider=provider_two.provider)
    assert AuthProvider.objects.filter(user_id=user.pk).count() == 2

    result = disconnect_auth_provider_use_case.execute(command=command)

    assert result is None
    assert AuthProvider.objects.filter(user_id=user.pk).count() == 1
    assert not AuthProvider.objects.filter(user_id=user.pk, provider=provider_two.provider).exists()


@pytest.mark.django_db
def test_disconnect_auth_provider_returns_none_if_successfully_disconnected_with_unusable_password_and_two_providers(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
    user: User,
):
    user.set_unusable_password()
    user.save()
    AuthProviderModelFactory.create(user=user, provider='github')
    provider_two = AuthProviderModelFactory.create(user=user, provider='google')
    command = DisconnectAuthProviderCommand(user_id=user.pk, provider=provider_two.provider)
    assert AuthProvider.objects.filter(user_id=user.pk).count() == 2

    result = disconnect_auth_provider_use_case.execute(command=command)

    assert result is None
    assert AuthProvider.objects.filter(user_id=user.pk).count() == 1
    assert not AuthProvider.objects.filter(user_id=user.pk, provider=provider_two.provider).exists()
    assert not user.has_usable_password()


@pytest.mark.django_db
def test_disconnect_auth_provider_returns_none_if_successfully_disconnected_with_usable_password_and_one_provider(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
    user: User,
):
    provider = AuthProviderModelFactory.create(user=user, provider='google')
    command = DisconnectAuthProviderCommand(user_id=user.pk, provider=provider.provider)
    assert AuthProvider.objects.filter(user_id=user.pk).count() == 1

    result = disconnect_auth_provider_use_case.execute(command=command)

    assert result is None
    assert AuthProvider.objects.filter(user_id=user.pk).count() == 0


def test_disconnect_auth_provider_not_supported_error_raised(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
):
    command = DisconnectAuthProviderCommand(user_id=1, provider='test_provider')
    with pytest.raises(AuthProviderNotSupportedError):
        disconnect_auth_provider_use_case.execute(command=command)


@pytest.mark.django_db
def test_disconnect_auth_provider_auth_providers_not_found_error_raised(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
    user: User,
):
    command = DisconnectAuthProviderCommand(user_id=user.pk, provider='google')
    with pytest.raises(AuthProvidersNotConnectedError):
        disconnect_auth_provider_use_case.execute(command=command)


@pytest.mark.django_db
def test_disconnect_auth_provider_auth_provider_not_connected_error_raised_if_requested_provider_is_not_connected(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
    user: User,
):
    AuthProviderModelFactory.create(user=user, provider='google')
    command = DisconnectAuthProviderCommand(user_id=user.pk, provider='github')
    with pytest.raises(AuthProviderNotConnectedError):
        disconnect_auth_provider_use_case.execute(command=command)


@pytest.mark.django_db
def test_disconnect_auth_unable_to_disconnect_auth_provivider_error_raised(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
    user: User,
):
    user.set_unusable_password()
    user.save()
    AuthProviderModelFactory.create(user=user, provider='google')
    command = DisconnectAuthProviderCommand(user_id=user.pk, provider='google')
    with pytest.raises(UnableToDisconnectAuthProviderError):
        disconnect_auth_provider_use_case.execute(command=command)


@pytest.mark.django_db
def test_disconnect_auth_provider_user_credentials_error_raised(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
):
    command = DisconnectAuthProviderCommand(user_id=None, provider='github')
    with pytest.raises(AuthCredentialsNotProvidedError):
        disconnect_auth_provider_use_case.execute(command=command)


@pytest.mark.django_db
def test_disconnect_auth_provider_user_not_found_error_raised(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
):
    command = DisconnectAuthProviderCommand(user_id=1, provider='github')
    with pytest.raises(UserNotFoundError):
        disconnect_auth_provider_use_case.execute(command=command)


@pytest.mark.django_db
def test_disconnect_auth_provider_user_not_active_error_raised(
    disconnect_auth_provider_use_case: DisconnectAuthProviderUseCase,
):
    user = UserModelFactory.create(is_active=False)
    command = DisconnectAuthProviderCommand(user_id=user.pk, provider='github')
    with pytest.raises(UserNotActiveError):
        disconnect_auth_provider_use_case.execute(command=command)
