from django.urls import path
from base import views

app_name = "base"

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<service_id>/", views.service_detail, name="service_detail"),
    path("book-appointment/<service_id>/<doctor_id>/", views.book_appointment, name="book_appointment"),
    path("checkout/<billing_id>/", views.checkout, name="checkout"),
    path("payment_status/<billing_id>/", views.payment_status, name="payment_status"),
    path("validate/<billing_id>/", views.validate, name="validate"),  # <-- add this
]