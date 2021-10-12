from django.urls import path, include
from .views import register, login, logout, activate, dashboard, forgotPassword, resetpassword_validate, resetPassword, \
    my_orders

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>', resetpassword_validate, name='resetpassword_validate'),
    path('forgotPassword/', forgotPassword, name='forgotPassword'),
    path('resetPassword/', resetPassword, name='resetPassword'),

    path('my_orders/', my_orders, name='my_orders'),

]
