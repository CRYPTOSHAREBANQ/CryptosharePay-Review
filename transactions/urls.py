from django.urls import path
from . import views

app_name = "businesses"

urlpatterns = [
    path('create-transaction/', views.CreateTransaction.as_view(), name="create"),
]