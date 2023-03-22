from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from duka.models import Category, Product
from duka.recommender import Recommender

from .forms import SearchForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    product_search_form = SearchForm()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if "query" in request.GET:
        query = request.GET["query"]
        if query:
            product_search_form = SearchForm(request.GET)
            if product_search_form.is_valid():
                query = product_search_form.cleaned_data["query"]
                search_vector = SearchVector("name", weight="A") + SearchVector(
                    "description", weight="B"
                )
                search_query = SearchQuery(query)
                products = (
                    products.annotate(
                        search=search_vector,
                        rank=SearchRank(search_vector, search_query),
                    )
                    .filter(search=search_query)
                    .order_by("-rank")
                )


                if not products:
                    # if product search has no results, return all products
                    messages.warning(request, "No product matching your search was found")
                    products = Product.objects.filter(available=True)
    return render(
        request,
        "duka/product/list.html",
        {
            "products": products,
            "category": category,
            "categories": categories,
            "product_search_form": product_search_form,
        },
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
