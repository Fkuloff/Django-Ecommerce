from django.urls import path, include
from .views import store

urlpatterns = [
    path('', store, name='store'),
    path('<slug:category_slug>', store, name='products_by_category'),
]
