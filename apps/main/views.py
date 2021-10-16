from django.shortcuts import render
from apps.store.models import Product, Variation, ProductGallery


def home(request):
    products = Product.objects.filter(is_available=True).order_by('created_date')

    variations = []
    gallery = []
    for p in products:
        variation = Variation.objects.filter(product=p).first()
        variations.append(variation)
        gallery_var = ProductGallery.objects.filter(variation=variation).first()
        gallery.append(gallery_var)

    context = {
        'products': products,
        'variations': variations,
        'gallery': gallery,
    }
    return render(request, 'index.html', context)
