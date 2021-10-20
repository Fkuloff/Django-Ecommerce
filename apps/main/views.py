from django.shortcuts import render
from apps.store.models import Product, Variation, ProductGallery


def home(request):
    products = Product.objects.filter(is_available=True).order_by('created_date')

    variations = []
    for p in products:
        variation = Variation.objects.filter(product=p).first()
        variations.append(variation)

    context = {
        'products': products,
        'variations': variations,
    }
    return render(request, 'index.html', context)
