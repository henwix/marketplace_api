from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.models import User


def data_to_user_entity(data: dict) -> UserEntity:
    return UserEntity(**data)


def user_to_entity(dto: User) -> UserEntity:
    entity = UserEntity(
        id=dto.pk,
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        phone=dto.phone,
        password=dto.password,
        avatar=dto.avatar,
        is_staff=dto.is_staff,
        is_active=dto.is_active,
        date_joined=dto.date_joined,
    )

    if 'seller_profile' in dto._state.fields_cache:
        entity.seller_profile = seller_to_entity(dto=getattr(dto, 'seller_profile', None))

    return entity


def user_from_entity(entity: UserEntity) -> User:
    return User(
        pk=entity.id,
        first_name=entity.first_name,
        last_name=entity.last_name,
        email=entity.email,
        phone=entity.phone,
        password=entity.password,
        avatar=entity.avatar,
        is_staff=entity.is_staff,
        is_active=entity.is_active,
        date_joined=entity.date_joined,
    )
