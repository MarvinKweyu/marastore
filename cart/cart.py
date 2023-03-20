from decimal import Decimal

from django.conf import settings

from coupons.models import Coupon
from duka.models import Product


class Cart(object):
    def __init__(self, request):
        """INitialize cart"""
        self.session = request.session
        # attempt get from session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # store current applied coupon
        self.coupon_id = self.session.get("coupon_id")

    def add(self, product, quantity: int = 1, override_quantity: bool = False):
        """add item to cart or update quantity"""
        product_id = str(product.id)  # since JSON allows only string keys
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                # convert from decimal to string to serialize
                "price": str(product.price),
            }

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        """save an item to the cart by marking the session as modified"""
        self.session.modified = True

    def remove(self, product):
        """Remove an item from the cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterate over the cart and get the products from the database"""
        product_ids = self.cart.keys()
        # get product objs and add to cart
        # make sure the product is available before returning?
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()  # copy current cart and add prod instances
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():  # against price and quant
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Count all items in cart"""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Get the total price of all items in the cart"""
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        """Remove cart from session"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """A coupon"""
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
