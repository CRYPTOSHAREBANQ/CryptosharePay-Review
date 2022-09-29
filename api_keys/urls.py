from django.urls import path
from . import views

app_name = "api_keys"

urlpatterns = [
    path('create-api-key/', views.CreateApiKey.as_view(), name="create"),
    path("get-api-keys/", views.GetApiKeys.as_view(), name="GetAllApiKeys"),
    path("activate_api_key/", views.ActivateApiKey.as_view(), name="ActivateApiKey"),
    path("deactivate-api-key/", views.DeactivateApiKey.as_view(), name="DeactivateApiKey"),
]