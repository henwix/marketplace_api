from django.db import models


class ProductsSearchOrderingEnum(models.TextChoices):
    CREATED_AT_ASC = 'created_at', 'Date of product creation ASC'
    CREATED_AT_DESC = '-created_at', 'Date of product creation DESC'
    UPDATED_AT_ASC = 'updated_at', 'Date of product update ASC'
    UPDATED_AT_DESC = '-updated_at', 'Date of product update DESC'
    PRICE_ASC = 'price', 'Product price ASC'
    PRICE_DESC = '-price', 'Product price DESC'
    REVIEWS_COUNT_ASC = 'reviews_count', 'Reviews count ASC'
    REVIEWS_COUNT_DESC = '-reviews_count', 'Reviews count DESC'
    REVIEWS_AVG_RATING_ASC = 'reviews_avg_rating', 'Reviews average rating ASC'
    REVIEWS_AVG_RATING_DESC = '-reviews_avg_rating', 'Reviews average rating DESC'
