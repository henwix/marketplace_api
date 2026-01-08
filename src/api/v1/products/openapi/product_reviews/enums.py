from django.db import models


class GetProductReviewsOrderingEnum(models.TextChoices):
    CREATED_AT_ASC = 'created_at', 'Date of product review creation ASC'
    CREATED_AT_DESC = '-created_at', 'Date of product review creation DESC'
    RATING_ASC = 'rating', 'Product review rating ASC'
    RATING_DESC = '-rating', 'Product review rating DESC'
