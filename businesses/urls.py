from django.urls import path
from . import views

app_name = "businesses"

urlpatterns = [
    path("all/", views.GetBusinesses.as_view(), name="GetAllBusinesses"),
]