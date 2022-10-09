from django.urls import path
from . import views

app_name = "protected"

urlpatterns = [
    path("accounts/email-has-account/", views.EmailHasAccount.as_view(), name="EmailHasAccount"),

    path("api-keys/api-key-no-account/<str:type>", views.GetAPIKeyNoAccount.as_view(), name="ApiKeyNoAccount"),
]