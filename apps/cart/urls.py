from django.urls import path, include
from .views import cart, add_cart, remove_cart, delete_cart_item, checkout, add_cart_item

urlpatterns = [
    path('', cart, name='cart'),

    path('add_cart/<int:variation_id>/', add_cart, name='add_cart'),

    path('add_cart_item/<int:item_id>/', add_cart_item, name='add_cart_item'),

    path('remove_cart/<int:variation_id>/<int:cart_item_id>/', remove_cart, name='remove_cart'),

    # path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', remove_cart_item, name='remove_cart_item'),

    path('checkout/', checkout, name='checkout')
]
