# class ProductReview(TimedBaseModel):
#     author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='product_reviews')
#     product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='reviews')
#     rating = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
#     text = models.TextField()

# TODO: ProductReviewImages
