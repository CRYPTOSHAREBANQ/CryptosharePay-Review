from django.urls import path
from transactions.payments import views as payments_views
from transactions.withdrawals import views as withdrawals_views
from transactions.automated import views as automated_views
# from . import views

app_name = "transactions"

urlpatterns = [

    ### <----- PAYMENTS -----> ###
    ### <----- PAYMENTS -----> ###

    path("payments/create/", payments_views.CreateTransactionDigitalToCrypto.as_view(), name="CreateTransaction"),
    path("payments/create/digital-to-crypto/", payments_views.CreateTransactionDigitalToCrypto.as_view(), name="CreateTransactionDigitalToCrypto"),
    # path("payments/create/crypto/", payments_views.CreateTransaction.as_view(), name="CreateTransaction"),
    path("payments/cancel/", payments_views.CancelTransaction.as_view(), name="CancelTransaction"),
    path("payments/complete/", payments_views.CompleteTransaction.as_view(), name="CancelTransaction"),
    path("payments/all/", payments_views.GetTransactions.as_view(), name="GetAllTransactions"),
    path("payments/filter/", payments_views.FilterTransactions.as_view(), name="FilterTransactions"),
    path("payments/<str:transaction_id>/", payments_views.GetTransaction.as_view(), name="GetTransaction"),

    ### <----- WITHDRAWALS -----> ###
    ### <----- WITHDRAWALS -----> ###

    path("withdrawals/create/", withdrawals_views.CreateWithdrawal.as_view(), name="CreateWithdrawal"),

    ### <----- AUTOMATED -----> ###
    ### <----- AUTOMATED -----> ###
    path("automated/payout-transactions/create/digital-to-crypto/", automated_views.CreateAutomatedPayoutDigitalToCrypto.as_view(), name="CreateAutomatedPayoutDigitalToCrypto"),
    # path("automated/cryptosharecredit/payout-transactions/create/digital-to-crypto/", automated_views.CreateAutomatedPayoutDigitalToCrypto.as_view(), name="CreateAutomatedPayoutDigitalToCrypto"),
    # path("automated/payout-transactions/create/crypto/", )

]