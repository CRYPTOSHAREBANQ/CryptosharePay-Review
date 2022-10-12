from django.urls import path
from . import views

app_name = "root"

urlpatterns = [
    path("ping/", views.Ping.as_view(), name="Ping"),
    path("cryptoapisverifydomain/", views.cryptoapis_verification, name="cryptoapis_verification")
    
]