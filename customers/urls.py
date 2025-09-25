from django.urls import path
from . import views

urlpatterns = [
    # simple example: list and create customers
    path('', views.CustomerListCreateView.as_view(), name='customer-list-create'),
    path('<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
]
