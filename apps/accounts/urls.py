from django.urls import path, include
from .views import register, login, logout, activate, dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),
]
