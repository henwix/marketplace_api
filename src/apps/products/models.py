# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.db import models
#
# from src.apps.common.models import TimedBaseModel
# from src.apps.users.models import User
#
#
# class Product(TimedBaseModel):
#     seller = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='products')
#     title = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     stock = models.PositiveIntegerField(default=0)
#     is_visible = models.BooleanField(default=True)
#
#
# class ProductReview(TimedBaseModel):
#     author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='product_reviews')
#     product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='reviews')
#     rating = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
#     text = models.TextField()


# ProductReviewImages
