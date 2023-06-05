from django.urls import path
from . import views

app_name = "protected"

urlpatterns = [
    path("accounts/email-has-account/", views.EmailHasAccount.as_view(), name="EmailHasAccount"),

    path("accounts/request-login-dashboard/", views.RequestLoginDashboard.as_view(), name="RequestLoginDashboard"),
    path("accounts/request-login-dashboard-individual/", views.IndividualRequestLoginDashboard.as_view(), name="IndividualRequestLoginDashboard"),
    # path("accounts/request-individual-login-dashboard/", views.RequestIndividualLoginDashboard, name="RequestIndividualLoginDashboard"),
    path("accounts/login-dashboard/", views.LoginDashboard.as_view(), name="LoginDashboard"),
    path("accounts/login-dashboard-individual/", views.LoginIndividualDashboard.as_view(), name="LoginDashboardIndividual"), 

    #SAME ENDPOINT
    path("api-keys/api-key-no-account/<str:type>", views.GetAPIKeyNoAccount.as_view(), name="ApiKeyNoAccount"),
    path("api-keys/api-key-no-account/<str:type>/", views.GetAPIKeyNoAccount.as_view(), name="ApiKeyNoAccount"),
    #SAME ENDPOINT

    path("transactions/automated/cancel-expired-transactions/", views.CancelExpiredTransactions.as_view(), name="CancelExpiredTransactions"),
    path("transactions/automated/execute-automated-transactions/", views.ExecuteAutomatedTransactions.as_view(), name="ExecuteAutomatedTransactions"),

    path("transactions/payments/<str:transaction_id>/", views.GetTransaction.as_view(), name="GetTransaction"),

    path("cryptocurrency/automated/update-exchange-rates/", views.UpdateExchangeRates.as_view(), name="UpdateExchangeRates"),

]