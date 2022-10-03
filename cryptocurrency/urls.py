from django.urls import path
from . import views

app_name = "businesses"

urlpatterns = [
    path("get-cryptocurrencies/", views.GetCryptocurrencies.as_view(), name="GetAllCryptocurrencies"),
    path("get-cryptocurrency/<str:code>/<str:network>/", views.GetCryptocurrency.as_view(), name="GetCryptocurrency"),
]