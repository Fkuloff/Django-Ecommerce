from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from apps.review.models import ReviewRating
from apps.order.models import OrderProduct
from .models import Product, VariationGallery, Variation, Size, Specification


def store(request):
    variations = Variation.objects.all()

    variations_count = len(variations)

    paginator = Paginator(variations, 10)
    page = request.GET.get('page')
    paged_variations = paginator.get_page(page)

    context = {
        'variations_count': variations_count,
        'variations': paged_variations,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, variation_vendor_code):
    try:
        variation = Variation.objects.get(vendor_code=variation_vendor_code)

        single_product = Product.objects.get(variation=variation)
        specifications = Specification.objects.filter(product=single_product)

        variations_of_single_product = Variation.objects.filter(product=single_product)

        product_gallery = VariationGallery.objects.filter(variation=variation)
        sizes = Size.objects.filter(variation=variation)

        order_product = OrderProduct.objects.filter(variation__product=single_product)

        reviews = ReviewRating.objects.filter(product=single_product, status=True)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'variations_of_single_product': variations_of_single_product,
        'order_product': order_product,
        'variation': variation,
        'sizes': sizes,
        'reviews': reviews,
        'specifications': specifications,
        'product_gallery': product_gallery,
    }

    return render(request, 'store/product_detail.html', context)


def search(request):
    variations = None
    variations_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        print(keyword)
        if keyword:
            variations = Variation.objects.filter(
                Q(product__description__icontains=keyword) | Q(product__product_name__icontains=keyword))
            variations_count = variations.count()
    context = {
        'variations': variations,
        'variations_count': variations_count,
    }
    return render(request, 'store/store.html', context)
