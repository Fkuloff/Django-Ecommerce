from django.urls import path

from .views import submit_review

urlpatterns = [
    path('<slug:single_product_id>', submit_review, name='submit_review')
]
