from cart.forms import CartAddProductForm
from django.shortcuts import get_object_or_404, render

from duka.models import Category, Product
from duka.recommender import Recommender


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        "duka/product/list.html",
        {"products": products, "category": category, "categories": categories},
    )


def product_detail(request, id, slug):
    # language = request.LANGUAGE_CODE
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()

    recommended_products = r.suggest_products_for([product], 4)

    return render(
        request,
        "duka/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )
