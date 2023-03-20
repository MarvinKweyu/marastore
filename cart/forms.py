from django import forms
from django.utils.translation import gettext_lazy as _

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Form for adding a product to cart"""

    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=_("Quantity")
    )
    # determine whether we are overriding an existing cart quantity or adding to it
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
