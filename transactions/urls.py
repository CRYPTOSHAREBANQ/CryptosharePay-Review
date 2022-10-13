from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    path("create/", views.CreateTransaction.as_view(), name="CreateTransaction"),
    path("all/", views.GetTransactions.as_view(), name="GetAllTransactions"),
    path("filter/", views.FilterTransactions.as_view(), name="FilterTransactions"),
    path("<str:transaction_id>/", views.GetTransaction.as_view(), name="GetTransaction"),


]