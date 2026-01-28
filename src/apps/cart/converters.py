from src.apps.cart.entities import CartEntity
from src.apps.cart.models import Cart


def cart_to_entity(dto: Cart) -> CartEntity:
    return CartEntity(
        id=dto.pk,
        user_id=dto.user_id,
    )
