import pytest
from punq import Container

from src.apps.authentication.commands.auth_providers import GetConnectedAuthProvidersCommand
from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.authentication.use_cases.auth_providers.get_connected_providers import GetConnectedAuthProvidersUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.authentication.auth_providers.factories import AuthProviderModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def get_connected_providers_use_case(container: Container) -> GetConnectedAuthProvidersUseCase:
    return container.resolve(GetConnectedAuthProvidersUseCase)


@pytest.mark.django_db
def test_get_connected_providers_returns_empty_list_if_no_connected_providers(
    get_connected_providers_use_case: GetConnectedAuthProvidersUseCase,
    user: User,
):
    command = GetConnectedAuthProvidersCommand(user_id=user.pk)
    result = get_connected_providers_use_case.execute(command=command)
    assert isinstance(result, list)
    assert len(result) == 0


@pytest.mark.django_db
@pytest.mark.parametrize('expected_providers_number', [1, 3, 5, 6, 7, 8, 10, 13, 17])
def test_get_connected_providers_returns_correct_data_(
    get_connected_providers_use_case: GetConnectedAuthProvidersUseCase,
    user: User,
    expected_providers_number: int,
):
    auth_providers = AuthProviderModelFactory.create_batch(size=expected_providers_number, user=user)

    command = GetConnectedAuthProvidersCommand(user_id=user.pk)
    retrieved_providers = get_connected_providers_use_case.execute(command=command)
    assert isinstance(retrieved_providers, list)
    assert len(retrieved_providers) == expected_providers_number

    for expected_auth_provider, retrieved_provider in zip(auth_providers, retrieved_providers, strict=True):
        assert expected_auth_provider.provider == retrieved_provider.provider
        assert expected_auth_provider.user_id == retrieved_provider.user_id
        assert expected_auth_provider.id == retrieved_provider.id
        assert expected_auth_provider.provider_uid == retrieved_provider.provider_uid
        assert expected_auth_provider.created_at == retrieved_provider.created_at
        assert expected_auth_provider.updated_at == retrieved_provider.updated_at


@pytest.mark.django_db
def test_get_connected_providers_user_credentials_error_raised(
    get_connected_providers_use_case: GetConnectedAuthProvidersUseCase,
):
    command = GetConnectedAuthProvidersCommand(user_id=None)
    with pytest.raises(AuthCredentialsNotProvidedError):
        get_connected_providers_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_connected_providers_user_not_found_error_raised(
    get_connected_providers_use_case: GetConnectedAuthProvidersUseCase,
):
    command = GetConnectedAuthProvidersCommand(user_id=1)
    with pytest.raises(UserNotFoundError):
        get_connected_providers_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_connected_providers_user_not_active_error_raised(
    get_connected_providers_use_case: GetConnectedAuthProvidersUseCase,
):
    user = UserModelFactory.create(is_active=False)
    command = GetConnectedAuthProvidersCommand(user_id=user.pk)
    with pytest.raises(UserNotActiveError):
        get_connected_providers_use_case.execute(command=command)
