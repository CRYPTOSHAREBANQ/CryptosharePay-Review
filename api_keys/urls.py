from django.urls import path
from . import views

app_name = "api_keys"

urlpatterns = [
    path('create_api_key/', views.CreateApiKey.as_view(), name="create"),
    path("get_api_keys/", views.GetApiKeys.as_view(), name="GetAllApiKeys"),
    path("activate_api_key/", views.ActivateApiKey.as_view(), name="ActivateApiKey"),
    path("deactivate_api_key/", views.DeactivateApiKey.as_view(), name="DeactivateApiKey"),
]