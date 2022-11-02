from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("create/", views.CreateAccount.as_view(), name="Create"),
    path("account-info/", views.GetAccount.as_view(), name="GetAccount"),
    path("request-customer-id/", views.RequestCustomerID.as_view(), name="RequestCustomerID"),
    path("account-customer-id/", views.GetAccountCustomerID.as_view(), name="GetAccountCustomerID"),
    # path("email-has-account/", views.EmailHasAccount.as_view(), name="EmailHasAccount"),
    # path("api-key-no-account/", views.GetAPIKeyNoAccount.as_view(), name="ApiKeyNoAccount"),
    # path("get-account-info/", views.GetAccountInfo.as_view(), name="GetAccountInfo"),
]