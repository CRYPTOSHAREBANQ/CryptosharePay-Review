from django.urls import path
from . import views

app_name = "businesses"

urlpatterns = [
    path('create/', views.CreateTransaction.as_view(), name="CreateTransaction"),
    path('<str:transaction_id>/', views.GetTransaction.as_view(), name="GetTransaction"),
    path('all/', views.GetTransactions.as_view(), name="all"),

]