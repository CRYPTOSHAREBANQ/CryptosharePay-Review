from django.urls import path
from . import views

app_name = "businesses"

urlpatterns = [
    path("<str:code>/<str:network>/", views.GetCryptocurrency.as_view(), name="GetCryptocurrency"),
    path("supported-cryptocurrencies/", views.GetCryptocurrencies.as_view(), name="GetAllCryptocurrencies"),
    
    path("supported-blockchains/", views.GetBlockchains.as_view(), name="GetAllBlockchains"),
    path("supported-networks/", views.GetNetworks.as_view(), name="GetAllNetworks"),
]