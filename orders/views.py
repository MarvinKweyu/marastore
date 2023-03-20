import weasyprint
from cart.cart import Cart
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem
from orders.tasks import order_created


def order_create(request):
    """Create an order view"""
    cart = Cart(request)

    if request.method == "POST":
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():

            order = order_form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                # create and save in single step
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
                cart.clear()  # clear cart
                # asynchronous task to send email
                order_created.delay(order.id)
                # set order insession
                request.session["order_id"] = order.id
                # go to payment
                return redirect(reverse("payment:process"))
                # return render(request, "orders/order/created.html", {"order": order})

    else:
        form = OrderCreateForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})


@staff_member_required
def admin_order_pdf(request, order_id):
    """Generate an invoice pdf from the admin section"""
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    #  specify filename to generate
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + "css/pdf.css")]
    )
    return response
