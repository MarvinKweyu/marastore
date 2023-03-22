from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path("process", views.payment_process, name="process"),
]
