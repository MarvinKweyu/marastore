from io import BytesIO

import weasyprint
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """Send an e-mail notification when an order is created successfully"""
    order = Order.objects.get(id=order_id)
    # create mail
    subject = f"maranomadstore - EE Invoice no. {order.id}"
    message = "Please , find attached the invoice for your recent purchase."
    email = EmailMessage(subject, message, "admin.maranomadstore.com", [order.email])
    # generate pdf and output to BytesIO instance - in-memory bytes buffer
    html = render_to_string("orders/order/pdf.html", {"order", order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + "css/pdf.css")]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach pdf file
    email.attach(f"order_{order.id}.pdf", out.getvalue(), "application/pdf")
    email.send()
