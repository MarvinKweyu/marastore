# from django.db import models

# from accounts.models import CustomUser
# from duka.models import Product


# class Cart(models.Model):
#     """Cart model"""

#     user = models.ForeignKey(
#         CustomUser, on_delete=models.CASCADE, null=True, blank=True
#     )
#     product = models.ManyToManyField(Product, through="CartItem")
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     paid = models.BooleanField(default=False)

#     class Meta:
#         ordering = ("-created",)
#         verbose_name = "Cart"
#         verbose_name_plural = "Carts"

#     def __str__(self):
#         return f"Cart {self.id}"

#     def get_total_cost(self):
#         return sum(item.price for item in self.product.all())

#     def get_total_items(self):
#         return sum(item.quantity for item in self.items.all())

#     def get_total_price(self):
#         return sum(item.get_price() for item in self.items.all())
