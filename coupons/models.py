from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    """MAnage coupons for discounts across orders"""

    code = models.CharField(unique=True, max_length=50)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # will be a percentage
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField()

    def __str__(self) -> str:
        return self.code
