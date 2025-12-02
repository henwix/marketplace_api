from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.models import Seller


def seller_to_entity(seller: Seller) -> SellerEntity:
    return SellerEntity(
        id=seller.id,
        user_id=seller.user_id,
        name=seller.name,
        description=seller.description,
        avatar=seller.avatar,
        background=seller.background,
    )


def seller_from_entity(seller_entity: SellerEntity) -> Seller:
    return Seller(
        pk=seller_entity.id,
        user_id=seller_entity.user_id,
        name=seller_entity.name,
        description=seller_entity.description,
        avatar=seller_entity.avatar,
        background=seller_entity.background,
    )
