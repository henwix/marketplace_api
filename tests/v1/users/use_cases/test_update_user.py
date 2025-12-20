import pytest
from punq import Container

from src.apps.users.converters import user_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import UserWithDataAlreadyExistsError
from src.apps.users.models import User
from src.apps.users.use_cases.update import UpdateUserUseCase
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def update_user_use_case(container: Container) -> UpdateUserUseCase:
    return container.resolve(UpdateUserUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames=['expected_first_name', 'expected_last_name', 'expected_email', 'expected_phone'],
    argvalues=[
        ('New Test First Name', 'New Test Last Name', 'new_email_test@test.com', '+8761276591245'),
        ('NewTestFirstName', 'NewTestLastName', 'ajsh1924c9h1casf@test.com', '+192715125124'),
    ],
)
def test_update_user(
    update_user_use_case: UpdateUserUseCase,
    user: User,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
):
    expected_data = {
        'first_name': expected_first_name,
        'last_name': expected_last_name,
        'email': expected_email,
        'phone': expected_phone,
    }
    updated_user = update_user_use_case.execute(user=user_to_entity(dto=user), data=expected_data)
    assert isinstance(updated_user, UserEntity)
    db_user = User.objects.get(pk=user.pk)
    assert user_to_entity(dto=db_user) == updated_user


@pytest.mark.django_db
def test_update_user_phone_already_exists_exception_raised(update_user_use_case: UpdateUserUseCase, user: User):
    expected_phone = '+592692652134'
    UserModelFactory.create(phone=expected_phone)

    with pytest.raises(UserWithDataAlreadyExistsError):
        update_user_use_case.execute(user=user_to_entity(dto=user), data={'phone': expected_phone})


@pytest.mark.django_db
def test_update_user_email_already_exists_exception_raised(update_user_use_case: UpdateUserUseCase, user: User):
    expected_email = 'sdjghksdhgsg@example.com'
    UserModelFactory.create(email=expected_email)

    with pytest.raises(UserWithDataAlreadyExistsError):
        update_user_use_case.execute(user=user_to_entity(dto=user), data={'email': expected_email})
