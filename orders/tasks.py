from celery import shared_task
from django.core.mail import send_mail

from orders.models import Order


@shared_task
def order_created(order_id):
    """
    Send an email notification when an order is successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order nr.{order.id}"
    message = f"Dear {order.first_name}, \n\n You have successfully placed an order. Your order ID is {order.id}"
    from_email = "admin.maranomadstore.com"
    recipient_list = [order.email]
    mail_sent = send_mail(subject, message, from_email, recipient_list)
    return mail_sent
