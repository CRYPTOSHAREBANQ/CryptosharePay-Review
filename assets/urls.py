from django.urls import path
from . import views

app_name = "assets"

urlpatterns = [
    path("all/", views.GetAssets.as_view(), name="GetAllAssets"),
    path("<str:cryptocurrency_code>/", views.GetAsset.as_view(), name="GetAsset"),
]