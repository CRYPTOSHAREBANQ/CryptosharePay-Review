from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("create/", views.CreateAccount.as_view(), name="Create"),
    path("email-has-account/", views.EmailHasAccount.as_view(), name="EmailHasAccount"),
]