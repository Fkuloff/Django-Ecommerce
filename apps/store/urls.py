from django.urls import path

from .views import store, product_detail, search

urlpatterns = [
    path('', store, name='store'),
    path('category/<slug:category_slug>/', store, name='products_by_category'),
    path('<slug:product_slug>/<slug:variation_vendor_code>/', product_detail, name='product_detail'),
    path('search/', search, name='search'),
]
