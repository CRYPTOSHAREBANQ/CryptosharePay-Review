from django.urls import path
from . import views

app_name = "webhooks"

urlpatterns = [
    path("cryptoapis/subscriptions/ConfirmedCoinTransactions/", views.cryptoapis_confirmed_coin_transactions, name="ConfirmedCoinTransactions"),
    # path("cryptoapis/callbacks/ConfirmationsCoinTransactions")
]