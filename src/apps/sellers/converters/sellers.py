from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.models import Seller


def data_to_seller_entity(data: dict) -> SellerEntity:
    return SellerEntity(**data)


def seller_to_entity(dto: Seller | None) -> SellerEntity | None:
    if dto is None:
        return None

    return SellerEntity(
        id=dto.pk,
        user_id=dto.user_id,
        name=dto.name,
        description=dto.description,
        avatar=dto.avatar,
        background=dto.background,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
    )


def seller_from_entity(entity: SellerEntity) -> Seller:
    return Seller(
        pk=entity.id,
        user_id=entity.user_id,
        name=entity.name,
        description=entity.description,
        avatar=entity.avatar,
        background=entity.background,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
