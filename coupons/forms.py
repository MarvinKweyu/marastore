from django import forms
from django.utils.translation import gettext_lazy as _

from coupons.models import Coupon


class CouponApplyForm(forms.Form):
    """Manage the entry of coupon code from the client"""

    code = forms.CharField(label=_("Coupon"))
