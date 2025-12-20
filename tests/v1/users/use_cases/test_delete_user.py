import pytest
from punq import Container

from src.apps.users.models import User
from src.apps.users.use_cases.delete import DeleteUserUseCase


@pytest.fixture
def delete_user_use_case(container: Container) -> DeleteUserUseCase:
    return container.resolve(DeleteUserUseCase)


@pytest.mark.django_db
def test_user_deleted(delete_user_use_case: DeleteUserUseCase, user: User):
    assert User.objects.filter(pk=user.pk).exists()
    delete_user_use_case.execute(user_id=user.pk)
    assert not User.objects.filter(pk=user.pk).exists()
