from django.urls import path, include
from .views import store

urlpatterns = [
    path('', store, name='homepage'),
]
