# catalog/urls.py
from django.urls import path
from .views import ProductUploadView, CategoryAveragePriceView, ProductListView

urlpatterns = [
    path('products/upload/', ProductUploadView.as_view(), name='product-upload'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('categories/<int:pk>/average-price/', CategoryAveragePriceView.as_view(), name='category-average-price'),
]
