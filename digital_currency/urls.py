from django.urls import path
from . import views

app_name = "digital_currency"

urlpatterns = [
    path("supported-digital-currencies/", views.GetDigitalCurrencies.as_view(), name="GetAllDigitalCurrencies"),
    path("get-digital-currency/<str:code>/", views.GetDigitalCurrency.as_view(), name="GetAllDigitalCurrency"),

]