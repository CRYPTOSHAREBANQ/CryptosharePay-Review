"""cryptosharepay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/accounts/', include('accounts.urls', namespace='accounts')),
    path('v1/businesses/', include('businesses.urls', namespace='businesses')),
    path('v1/api-keys/', include('api_keys.urls', namespace='api_keys')),
    path('v1/cryptocurrency/', include('cryptocurrency.urls', namespace='cryptocurrency')),
    path('v1/digital-currency/', include('digital_currency.urls', namespace='digital_currency')),
    path('v1/transactions/', include('transactions.urls', namespace='transactions')),

    path('protected/', include('protected.urls', namespace='protected')),

]
