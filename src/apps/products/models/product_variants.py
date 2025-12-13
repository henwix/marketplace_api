from decimal import Decimal
from uuid import uuid7

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.common.models import TimedBaseModel
from src.apps.products.models.products import Product


class ProductVariant(TimedBaseModel):
    id = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid7, help_text=_('Product variant uuid')
    )
    product = models.ForeignKey(
        verbose_name=_('product'), to=Product, on_delete=models.CASCADE, related_name='variants'
    )
    title = models.CharField(_('title'), max_length=200, help_text=_('Product variant title'))
    price = models.DecimalField(
        _('price'),
        db_index=True,
        max_digits=10,
        decimal_places=2,
        help_text=_('Product variant price'),
        validators=[MinValueValidator(Decimal('0.10'))],
    )
    stock = models.PositiveIntegerField(_('stock'), default=0, db_index=True, help_text=_('Product variant in stock'))
    is_visible = models.BooleanField(
        _('is visible'), default=True, db_index=True, help_text=_('Is product variant visible')
    )

    class Meta:
        verbose_name = 'Product variant'
        verbose_name_plural = 'Product variants'
