from django.contrib import admin
from django.urls import path, include
from .views import place_order

urlpatterns = [
    path('place_order/', place_order, name='place_order')
]
