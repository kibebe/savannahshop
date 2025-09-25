"""
URL configuration for savannahshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from mozilla_django_oidc import views as oidc_views
from django.contrib.auth.views import LogoutView
from mozilla_django_oidc.views import OIDCLogoutView
from auth_service import views


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # Customers
        'customers': reverse('customer-list-create', request=request, format=format),

        # Orders
        'orders': reverse('order-list-create', request=request, format=format),

        # Catalog
        'upload-product': reverse('product-upload', request=request, format=format),
        'product-list': reverse('product-list', request=request, format=format),
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('api/orders/', include('orders.urls')),
    path('api/customers/', include('customers.urls')),
    path('api/catalog/', include('catalog.urls')),
    path("oidc/", include("mozilla_django_oidc.urls")),
]
