from django.urls import path
from coupons import views

app_name = "coupons"
urlpatterns = [
    path("apply/", views.apply_coupon, name="apply_coupon"),
]
