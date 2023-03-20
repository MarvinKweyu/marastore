import braintree
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from orders.models import Order

from .tasks import payment_completed

# braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


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
            return redirect("payment:done")
        else:
            return redirect("payment:canceled")
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(
            request,
            "payment/process.html",
            {"order": order, "client_token": client_token},
        )


def payment_done(request):
    return render(request, "payment/done.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")
