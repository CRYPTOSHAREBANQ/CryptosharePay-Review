from django.urls import path
from . import views

app_name = "webhooks"

urlpatterns = [
    path("cryptoapis/subscriptions/ConfirmedCoinTransactions/", views.cryptoapis_confirmed_coin_transactions, name="ConfirmedCoinTransactions"),
    path("cryptoapis/subscriptions/ConfirmedTokenTransactions/", views.cryptoapis_confirmed_token_transactions, name="ConfirmedCoinTransactions"),
    # /cryptoapis/subscriptions/ConfirmedTokenTransactions/
    # path("cryptoapis/callbacks/ConfirmationsCoinTransactions")
]