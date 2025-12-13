from uuid import uuid7

from django.contrib.postgres.indexes import GinIndex, Index, OpClass
from django.db import models
from django.db.models.functions import Upper
from django.utils.translation import gettext_lazy as _

from src.apps.common.models import TimedBaseModel
from src.apps.sellers.models import Seller


class Product(TimedBaseModel):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid7, help_text=_('Product uuid'))
    slug = models.SlugField(_('slug'), unique=True, max_length=300, help_text=_('Product slug'))
    seller = models.ForeignKey(to=Seller, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(_('title'), max_length=255, help_text=_('Product title'))
    description = models.TextField(_('description'), blank=True, null=True, help_text=_('Product description'))
    short_description = models.CharField(
        _('short description'), max_length=500, blank=True, null=True, help_text=_('Short product description')
    )
    is_visible = models.BooleanField(_('is visible'), default=True, help_text=_('Is product visible'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            Index(fields=['created_at']),
            Index(fields=['updated_at']),
            GinIndex(
                OpClass(Upper('title'), name='gin_trgm_ops'),
                name='product_title_trgm_gin_idx',
            ),
            GinIndex(
                OpClass(Upper('description'), name='gin_trgm_ops'),
                name='product_desc_trgm_gin_idx',
            ),
            GinIndex(
                OpClass(Upper('short_description'), name='gin_trgm_ops'),
                name='product_short_desc_trgm_idx',
            ),
        ]


# TODO: ProductImages
