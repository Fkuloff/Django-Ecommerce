from django.shortcuts import render
from apps.store.models import Product, Variation
from apps.store.models import ReviewRating


def home(request):
    products = Product.objects.filter(is_available=True).order_by('created_date')

    context = {
        'products': products,
    }
    return render(request, 'home.html', context)
