from django.urls import path, include
from .views import submit_review

urlpatterns = [
    path('<int:variation_vendor_code>', submit_review, name='submit_review')
]
