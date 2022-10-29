from django.urls import path
from . import views

app_name = "digital_currency"

urlpatterns = [
    path("supported-digital-currencies/", views.GetDigitalCurrencies.as_view(), name="GetAllDigitalCurrencies"),
    path("<str:digital_currency_code>/", views.GetDigitalCurrency.as_view(), name="GetAllDigitalCurrency"),

]