from django.urls import path

from .views import submit_review

urlpatterns = [
    path('<slug:variation_vendor_code>', submit_review, name='submit_review')
]
