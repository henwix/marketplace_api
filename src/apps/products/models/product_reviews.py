from django.contrib.postgres.indexes import Index
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.common.models import TimedBaseModel
from src.apps.products.models.products import Product
from src.apps.users.models import User


class ProductReview(TimedBaseModel):
    user = models.ForeignKey(
        verbose_name=_('user'),
        to=User,
        on_delete=models.CASCADE,
        related_name='product_reviews',
    )
    product = models.ForeignKey(
        verbose_name=_('product'),
        to=Product,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.SmallIntegerField(
        verbose_name=_('rating'),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Review rating'),
    )
    text = models.TextField(
        verbose_name=_('text'),
        help_text=_('Review text'),
    )

    class Meta:
        verbose_name = 'Product review'
        verbose_name_plural = 'Product reviews'
        indexes = [
            Index(fields=['product_id', 'created_at']),
            Index(fields=['product_id', 'rating']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_product_review',
            )
        ]


# TODO: ProductReviewImages
