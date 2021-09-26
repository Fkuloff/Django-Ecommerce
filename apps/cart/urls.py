from django.urls import path, include
from .views import cart, add_cart

urlpatterns = [
    path('', cart, name='cart'),
    path('add/<int:product_id>', add_cart, name='add_cart')
]
