from uuid import uuid4

import pytest
from punq import Container

from src.apps.authentication.entities.social_account import SocialAccountEntity
from src.apps.authentication.exceptions.social_account import SocialAccountProviderAlreadyConnectedError
from src.apps.authentication.models.social_account import SocialAccount
from src.apps.authentication.repositories.social_account import BaseSocialAccountRepository
from src.apps.users.models import User
from tests.v1.authentication.oauth.factories import SocialAccountModelFactory


@pytest.fixture
def social_account_repository(container: Container) -> BaseSocialAccountRepository:
    return container.resolve(BaseSocialAccountRepository)


@pytest.mark.django_db
def test_get_provivder_by_uid_and_name_returns_provider_entity(
    social_account_repository: BaseSocialAccountRepository,
    social_account: SocialAccount,
):
    social_account_entity = social_account_repository.get_by_provider_uid_and_name(
        provider_uid=social_account.provider_uid,
        provider=social_account.provider,
    )
    assert isinstance(social_account_entity, SocialAccountEntity)
    assert social_account_entity.id == social_account.pk
    assert social_account_entity.user_id == social_account.user_id
    assert social_account_entity.provider == social_account.provider
    assert social_account_entity.provider_uid == social_account.provider_uid
    assert social_account_entity.created_at == social_account.created_at
    assert social_account_entity.updated_at == social_account.updated_at


@pytest.mark.django_db
def test_get_provivder_by_uid_and_name_returns_none_if_provider_does_not_exist(
    social_account_repository: BaseSocialAccountRepository,
):
    assert (
        social_account_repository.get_by_provider_uid_and_name(provider_uid=uuid4().hex, provider='test_provider')
        is None
    )


@pytest.mark.django_db
def test_social_account_successfully_saved(
    social_account_repository: BaseSocialAccountRepository,
    user: User,
):
    exepected_provider_uid = uuid4().hex
    exepected_provider = 'test_provider'
    assert SocialAccount.objects.count() == 0
    new_social_account_entity = SocialAccountEntity.create(
        user_id=user.pk,
        provider=exepected_provider,
        provider_uid=exepected_provider_uid,
    )

    created_social_account = social_account_repository.save(social_account=new_social_account_entity, update=False)

    assert isinstance(created_social_account, SocialAccountEntity)
    assert SocialAccount.objects.filter(
        user_id=user.pk,
        provider=exepected_provider,
        provider_uid=exepected_provider_uid,
    ).exists()


@pytest.mark.django_db
def test_social_account_not_saved_with_sane_name_and_uid_and_social_account_provider_already_connected_error_raised(
    social_account_repository: BaseSocialAccountRepository,
    social_account: SocialAccount,
):
    new_social_account_entity = SocialAccountEntity.create(
        user_id=social_account.user_id,
        provider=social_account.provider,
        provider_uid=social_account.provider_uid,
    )
    with pytest.raises(SocialAccountProviderAlreadyConnectedError):
        social_account_repository.save(social_account=new_social_account_entity, update=False)


@pytest.mark.django_db
def test_social_account_not_saved_with_same_name_and_social_account_provider_already_connected_error_raised(
    social_account_repository: BaseSocialAccountRepository,
    social_account: SocialAccount,
):
    new_social_account_entity = SocialAccountEntity.create(
        user_id=social_account.user_id,
        provider=social_account.provider,
        provider_uid=uuid4().hex,
    )
    with pytest.raises(SocialAccountProviderAlreadyConnectedError):
        social_account_repository.save(social_account=new_social_account_entity, update=False)


@pytest.mark.django_db
def test_get_many_by_user_id_returns_empty_list_if_no_connected_providers(
    social_account_repository: BaseSocialAccountRepository,
    user: User,
):
    result = social_account_repository.get_many_by_user_id(user_id=user.pk)
    assert isinstance(result, list)
    assert len(result) == 0


@pytest.mark.django_db
@pytest.mark.parametrize('expected_providers_number', [1, 3, 5, 6, 7, 8, 10, 13, 17])
def test_get_many_by_user_id_returns_correct_data_(
    social_account_repository: BaseSocialAccountRepository,
    user: User,
    expected_providers_number: int,
):
    social_accounts = SocialAccountModelFactory.create_batch(size=expected_providers_number, user=user)

    retrieved_social_accounts = social_account_repository.get_many_by_user_id(user_id=user.pk)
    assert isinstance(retrieved_social_accounts, list)
    assert len(retrieved_social_accounts) == expected_providers_number

    for expected_social_account, retrieved_social_account in zip(
        social_accounts, retrieved_social_accounts, strict=True
    ):
        assert expected_social_account.provider == retrieved_social_account.provider
        assert expected_social_account.user_id == retrieved_social_account.user_id
        assert expected_social_account.id == retrieved_social_account.id
        assert expected_social_account.provider_uid == retrieved_social_account.provider_uid
        assert expected_social_account.created_at == retrieved_social_account.created_at
        assert expected_social_account.updated_at == retrieved_social_account.updated_at
