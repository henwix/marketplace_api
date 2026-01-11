from decimal import Decimal
from uuid import uuid7

from django.contrib.postgres.indexes import GinIndex, Index, OpClass
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Upper
from django.utils.translation import gettext_lazy as _

from src.apps.common.models import TimedBaseModel
from src.apps.sellers.models import Seller


class Product(TimedBaseModel):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid7,
        help_text=_('Product uuid'),
    )
    slug = models.SlugField(
        verbose_name=_('slug'),
        unique=True,
        max_length=300,
        help_text=_('Product slug'),
    )
    seller = models.ForeignKey(
        verbose_name=_('seller'),
        to=Seller,
        on_delete=models.CASCADE,
        related_name='products',
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        help_text=_('Product title'),
    )
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
        help_text=_('Product description'),
    )
    short_description = models.CharField(
        verbose_name=_('short description'),
        max_length=500,
        blank=True,
        help_text=_('Short product description'),
    )
    is_visible = models.BooleanField(
        verbose_name=_('is visible'),
        default=True,
        help_text=_('Is product visible'),
    )

    reviews_count = models.PositiveIntegerField(
        verbose_name=_('reviews count'),
        default=0,
        help_text=_('Reviews count'),
    )
    reviews_avg_rating = models.DecimalField(
        verbose_name=_('reviews average rating'),
        max_digits=3,
        decimal_places=2,
        default=Decimal('0'),
        help_text=_('Reviews average rating'),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            Index(fields=['created_at']),
            Index(fields=['updated_at']),
            Index(fields=['reviews_count']),
            Index(fields=['reviews_avg_rating']),
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
