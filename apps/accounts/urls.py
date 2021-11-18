from django.urls import path

from .views import register, login, logout, activate, dashboard, forgot_password, reset_password_validate, reset_password, \
    my_orders, change_password, order_detail, edit_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>', reset_password_validate, name='resetpassword_validate'),
    path('forgotPassword/', forgot_password, name='forgotPassword'),
    path('resetPassword/', reset_password, name='resetPassword'),

    path('my_orders/', my_orders, name='my_orders'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),

]
