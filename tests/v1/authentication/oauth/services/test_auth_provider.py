from uuid import uuid4

import pytest
from punq import Container

from src.apps.authentication.entities.auth_providers import AuthProviderEntity
from src.apps.authentication.exceptions.auth_providers import AuthProviderAlreadyConnectedError
from src.apps.authentication.models.auth_provider import AuthProvider
from src.apps.authentication.services.auth_providers import BaseAuthProviderService
from src.apps.users.models import User
from tests.v1.authentication.oauth.factories import AuthProviderModelFactory


@pytest.fixture
def auth_provider_service(container: Container) -> BaseAuthProviderService:
    return container.resolve(BaseAuthProviderService)


@pytest.mark.django_db
def test_get_provivder_by_uid_and_name_returns_provider_entity(
    auth_provider_service: BaseAuthProviderService,
    auth_provider: AuthProvider,
):
    auth_provider_entity = auth_provider_service.get_by_provider_uid_and_name(
        provider_uid=auth_provider.provider_uid,
        provider=auth_provider.provider,
    )
    assert isinstance(auth_provider_entity, AuthProviderEntity)
    assert auth_provider_entity.id == auth_provider.pk
    assert auth_provider_entity.user_id == auth_provider.user_id
    assert auth_provider_entity.provider == auth_provider.provider
    assert auth_provider_entity.provider_uid == auth_provider.provider_uid
    assert auth_provider_entity.created_at == auth_provider.created_at
    assert auth_provider_entity.updated_at == auth_provider.updated_at


@pytest.mark.django_db
def test_get_provivder_by_uid_and_name_returns_none_if_provider_does_not_exist(
    auth_provider_service: BaseAuthProviderService,
):
    assert (
        auth_provider_service.get_by_provider_uid_and_name(provider_uid=uuid4().hex, provider='test_provider') is None
    )


@pytest.mark.django_db
def test_auth_provider_successfully_saved(
    auth_provider_service: BaseAuthProviderService,
    user: User,
):
    exepected_provider_uid = uuid4().hex
    exepected_provider = 'test_provider'
    assert AuthProvider.objects.count() == 0
    new_auth_provider_entity = AuthProviderEntity.create(
        user_id=user.pk,
        provider=exepected_provider,
        provider_uid=exepected_provider_uid,
    )

    created_auth_provider = auth_provider_service.save(auth_provider=new_auth_provider_entity, update=False)

    assert isinstance(created_auth_provider, AuthProviderEntity)
    assert AuthProvider.objects.filter(
        user_id=user.pk,
        provider=exepected_provider,
        provider_uid=exepected_provider_uid,
    ).exists()


@pytest.mark.django_db
def test_auth_provider_not_saved_with_sane_name_and_uid_and_auth_provider_provider_already_connected_error_raised(
    auth_provider_service: BaseAuthProviderService,
    auth_provider: AuthProvider,
):
    new_auth_provider_entity = AuthProviderEntity.create(
        user_id=auth_provider.user_id,
        provider=auth_provider.provider,
        provider_uid=auth_provider.provider_uid,
    )
    with pytest.raises(AuthProviderAlreadyConnectedError):
        auth_provider_service.save(auth_provider=new_auth_provider_entity, update=False)


@pytest.mark.django_db
def test_auth_provider_not_saved_with_same_name_and_auth_provider_provider_already_connected_error_raised(
    auth_provider_service: BaseAuthProviderService,
    auth_provider: AuthProvider,
):
    new_auth_provider_entity = AuthProviderEntity.create(
        user_id=auth_provider.user_id,
        provider=auth_provider.provider,
        provider_uid=uuid4().hex,
    )
    with pytest.raises(AuthProviderAlreadyConnectedError):
        auth_provider_service.save(auth_provider=new_auth_provider_entity, update=False)


@pytest.mark.django_db
def test_get_many_by_user_id_returns_empty_list_if_no_connected_providers(
    auth_provider_service: BaseAuthProviderService,
    user: User,
):
    result = auth_provider_service.get_many_by_user_id(user_id=user.pk)
    assert isinstance(result, list)
    assert len(result) == 0


@pytest.mark.django_db
@pytest.mark.parametrize('expected_providers_number', [1, 3, 5, 6, 7, 8, 10, 13, 17])
def test_get_many_by_user_id_returns_correct_data_(
    auth_provider_service: BaseAuthProviderService,
    user: User,
    expected_providers_number: int,
):
    auth_providers = AuthProviderModelFactory.create_batch(size=expected_providers_number, user=user)

    retrieved_auth_providers = auth_provider_service.get_many_by_user_id(user_id=user.pk)
    assert isinstance(retrieved_auth_providers, list)
    assert len(retrieved_auth_providers) == expected_providers_number

    for expected_auth_provider, retrieved_auth_provider in zip(auth_providers, retrieved_auth_providers, strict=True):
        assert expected_auth_provider.provider == retrieved_auth_provider.provider
        assert expected_auth_provider.user_id == retrieved_auth_provider.user_id
        assert expected_auth_provider.id == retrieved_auth_provider.id
        assert expected_auth_provider.provider_uid == retrieved_auth_provider.provider_uid
        assert expected_auth_provider.created_at == retrieved_auth_provider.created_at
        assert expected_auth_provider.updated_at == retrieved_auth_provider.updated_at
