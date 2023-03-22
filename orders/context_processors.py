from orders.models import Order


def user_has_orders(request):
    """Orders of the current user"""
    if request.user.is_authenticated:
        return {"user_orders": Order.objects.filter(user=request.user)}
    return {"user_orders": None}
