from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.products.models.product_variants import ProductVariant
from src.apps.sellers.models import Seller
from src.apps.users.models import User


class Cart(models.Model):
    user = models.OneToOneField(
        verbose_name=_('user'),
        help_text=_('User related to this Cart'),
        to=User,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    product_variants = models.ManyToManyField(
        verbose_name=_('product variants'),
        help_text=_('Product variants related to this Cart'),
        to=ProductVariant,
        through='CartItem',
    )

    def __str__(self):
        return f'Cart for User #{self.user_id}'

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')


class CartItem(models.Model):
    cart = models.ForeignKey(
        verbose_name=_('cart'),
        help_text=_('Cart related to this CartItem'),
        to=Cart,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product_variant = models.ForeignKey(
        verbose_name=_('product variant'),
        help_text=_('Product Variant related to this CartItem'),
        to=ProductVariant,
        on_delete=models.CASCADE,
    )
    seller = models.ForeignKey(
        verbose_name=_('seller'),
        help_text=_('Seller related to this CartItem'),
        to=Seller,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_('quantity'),
        help_text=_('Product variant quantity'),
        validators=[MinValueValidator(1)],
    )
    price_snapshot = models.DecimalField(
        verbose_name=_('price snapshot'),
        help_text=_('Product variant price snapshot'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.10'))],
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        help_text=_('Date of creation'),
        auto_now_add=True,
    )

    def __str__(self):
        return f'Item №{self.pk} for Cart №{self.cart_id}'

    class Meta:
        verbose_name = _('CartItem')
        verbose_name_plural = _('CartItems')
