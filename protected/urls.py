from django.urls import path
from . import views

app_name = "protected"

urlpatterns = [
    path("accounts/email-has-account/", views.EmailHasAccount.as_view(), name="EmailHasAccount"),

    path("api-keys/api-key-no-account/<str:type>/", views.GetAPIKeyNoAccount.as_view(), name="ApiKeyNoAccount"),

    path("transactions/automated/cancel-expired-transactions/", views.CancelExpiredTransactions.as_view(), name="CancelExpiredTransactions"),

    path("transactions/payments/<str:transaction_id>/", views.GetTransaction.as_view(), name="GetTransaction"),

    path("cryptocurrency/automated/update-exchange-rates/", views.UpdateExchangeRates.as_view(), name="UpdateExchangeRates"),

]