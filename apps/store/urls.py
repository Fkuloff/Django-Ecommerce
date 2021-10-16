from django.urls import path, include
from .views import store, product_detail, search, submit_review

urlpatterns = [
    path('', store, name='store'),
    path('category/<slug:category_slug>/', store, name='products_by_category'),
    path('<slug:product_slug>/<int:variation_vendor_code>/', product_detail, name='product_detail'),
    path('search/', search, name='search'),
    path('submit_review/<int:product_id>', submit_review, name='submit_review')
]
