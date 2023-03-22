from decimal import Decimal

from coupons.models import Coupon
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from duka.models import Product
from accounts.models import CustomUser


class Order(models.Model):
    """Manage all orders across the system"""

    user = models.ForeignKey(CustomUser, related_name="orders", on_delete=models.CASCADE)
    city = models.CharField(_("city"), max_length=250)
    address = models.CharField(_("address"), max_length=250)
    postal_code = models.CharField(_("postal code"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    # if coupon is deleted, set coupon to null but retain the discount
    coupon = models.ForeignKey(
        Coupon, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))


class OrderItem(models.Model):
    """Items in an order"""

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return super().__str__()

    def get_cost(self):
        """Return total cost of an item"""
        return self.price * self.quantity
