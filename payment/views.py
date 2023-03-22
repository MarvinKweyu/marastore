import braintree
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order

from .tasks import payment_completed

# braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


@login_required
def payment_process(request):
    order_id = request.session.get("order_id")  # stored from order_create view
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == "POST":
        # GET NONCE
        nonce = request.POST.get("payment_method_nonce", None)
        # /create and submit transaction
        result = gateway.transaction.sale(
            {
                "amount": f"{total_cost: .2f}",
                "payment_method_nonce": nonce,  # from template with braintree SDK
                "options": {"submit_for_settlement": True},
            }
        )

        if result.is_success:
            order.paid = True
            # store transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # launch asyn task
            payment_completed.delay(order.id)
            messages.success(
                request,
                f"Your order has been created successfully: Order id {order.id}",
            )

            return redirect("duka:product_list")
        else:
            messages.warning(request, "There was an error processing your order")
            return redirect("duka:product_list")
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(
            request,
            "payment/process.html",
            {"order": order, "client_token": client_token},
        )
