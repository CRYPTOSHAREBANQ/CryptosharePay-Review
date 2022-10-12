from django.urls import path
from . import views

app_name = "businesses"

urlpatterns = [
    path('create/', views.CreateTransaction.as_view(), name="create"),
    path('all/', views.GetTransactions.as_view(), name="all"),
]