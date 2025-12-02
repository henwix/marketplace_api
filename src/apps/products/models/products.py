from uuid import uuid7

from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.common.models import TimedBaseModel
from src.apps.sellers.models import Seller


class Product(TimedBaseModel):
    uuid = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid7, help_text=_('Product uuid'))
    slug = models.SlugField(_('slug'), unique=True, max_length=300, help_text=_('Product slug'))
    seller = models.ForeignKey(to=Seller, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(_('title'), max_length=255, db_index=True, help_text=_('Product title'))
    description = models.TextField(_('description'), blank=True, null=True, help_text=_('Product description'))
    short_description = models.CharField(
        _('short description'), max_length=500, blank=True, null=True, help_text=_('Short product description')
    )
    is_visible = models.BooleanField(_('is visible'), default=True, db_index=True, help_text=_('Is product visible'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductVariant(TimedBaseModel):
    uuid = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid7, help_text=_('Product variant uuid')
    )
    product = models.ForeignKey(
        verbose_name=_('product'), to=Product, on_delete=models.CASCADE, related_name='variants'
    )
    title = models.CharField(_('title'), max_length=200, help_text=_('Product variant title'))
    price = models.DecimalField(
        _('price'), db_index=True, max_digits=10, decimal_places=2, help_text=_('Product variant price')
    )
    stock = models.PositiveIntegerField(_('stock'), default=0, db_index=True, help_text=_('Product variant in stock'))
    is_visible = models.BooleanField(
        _('is visible'), default=True, db_index=True, help_text=_('Is product variant visible')
    )

    class Meta:
        verbose_name = 'Product variant'
        verbose_name_plural = 'Product variants'


# TODO: move to reviews.py file
# class ProductReview(TimedBaseModel):
#     author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='product_reviews')
#     product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='reviews')
#     rating = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
#     text = models.TextField()

# ProductImages
# ProductReviewImages
