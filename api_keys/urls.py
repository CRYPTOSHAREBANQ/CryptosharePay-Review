from django.urls import path
from . import views

app_name = "api_keys"

urlpatterns = [
    path("all/", views.GetApiKeys.as_view(), name="GetAllApiKeys"),
    path("get-by-business-id/", views.GetApiKey.as_view(), name="GetApiKey"),
    path('create/', views.CreateApiKey.as_view(), name="create"),
    path("activate/", views.ActivateApiKey.as_view(), name="ActivateApiKey"),
    path("deactivate/", views.DeactivateApiKey.as_view(), name="DeactivateApiKey"),
]