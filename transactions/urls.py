from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    path("payments/create/", views.CreateTransaction.as_view(), name="CreateTransaction"),
    path("payments/all/", views.GetTransactions.as_view(), name="GetAllTransactions"),
    path("payments/filter/", views.FilterTransactions.as_view(), name="FilterTransactions"),
    path("payments/<str:transaction_id>/", views.GetTransaction.as_view(), name="GetTransaction"),


]