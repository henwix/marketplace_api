import jwt
import pytest
from django.conf import settings
from punq import Container

from src.apps.authentication.exceptions.jwt import JWTTokenInvalidError
from src.apps.authentication.services.jwt import BaseJWTService
from src.apps.users.converters import user_to_entity
from src.apps.users.models import User


@pytest.fixture
def jwt_service(container: Container) -> BaseJWTService:
    return container.resolve(BaseJWTService)


@pytest.mark.django_db
def test_create_tokens_returns_dict_with_valid_tokens(
    jwt_service: BaseJWTService,
    user: User,
):
    tokens = jwt_service.create_tokens(user=user_to_entity(dto=user))
    assert isinstance(tokens, dict)
    assert 'access' in tokens
    assert 'refresh' in tokens

    decoded_access_token = jwt.decode(jwt=tokens['access'], key=settings.SECRET_KEY, algorithms=['HS256'])
    decoded_refresh_token = jwt.decode(jwt=tokens['refresh'], key=settings.SECRET_KEY, algorithms=['HS256'])

    assert decoded_access_token['user_id'] == str(user.pk)
    assert decoded_refresh_token['user_id'] == str(user.pk)
    assert decoded_access_token['token_type'] == 'access'
    assert decoded_refresh_token['token_type'] == 'refresh'


@pytest.mark.django_db
def test_token_decoded_without_signature_verification(
    jwt_service: BaseJWTService,
    user: User,
):
    tokens = jwt_service.create_tokens(user=user_to_entity(dto=user))
    payload = jwt_service.decode_unverified(token=tokens['access'])

    for i in ['token_type', 'exp', 'iat', 'jti', 'user_id']:
        assert i in payload


def test_token_not_decoded_and_jwt_invalid_token_error_raised_if_invalid_token_format(
    jwt_service: BaseJWTService,
):
    with pytest.raises(JWTTokenInvalidError):
        jwt_service.decode_unverified(token='123')
