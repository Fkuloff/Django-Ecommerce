from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from apps.review.models import ReviewRating
from .models import Product, VariationGallery, Variation, Size, Specification


def store(request):
    products = Product.objects.filter(is_available=True).order_by('created_date')

    variations = []
    for p in products:
        variation = Variation.objects.filter(product=p).first()
        variations.append(variation)

    # if category_slug is not None:
    #     categories = get_object_or_404(Category, slug=category_slug)
    #     products = Product.objects.filter(category=categories, is_available=True)
    #     product_count = products.count()
    #
    #     paginator = Paginator(products, 10)
    #     page = request.GET.get('page')
    #     paged_products = paginator.get_page(page)
    #
    # else:
    # products = Product.objects.filter(is_available=True).order_by('-id')
    variations_count = len(variations)

    paginator = Paginator(variations, 10)
    page = request.GET.get('page')
    paged_variations = paginator.get_page(page)

    context = {
        'variations_count': variations_count,
        'variations': paged_variations,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, product_slug, variation_vendor_code):
    try:
        single_product = Product.objects.get(slug=product_slug)
        specifications = Specification.objects.filter(product=single_product)

        variations_of_single_product = Variation.objects.filter(product=single_product)

        variation = Variation.objects.get(vendor_code=variation_vendor_code)

        product_gallery = VariationGallery.objects.filter(variation=variation)
        sizes = Size.objects.filter(variation=variation)
    except Exception as e:
        raise e

    reviews = ReviewRating.objects.filter(variation=variation, status=True)

    context = {
        'single_product': single_product,
        'variations_of_single_product': variations_of_single_product,

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
        if keyword:
            variations = Variation.objects.order_by('-created_date').filter(
                Q(product__description__icontains=keyword) | Q(product__product_name__icontains=keyword))
            variations_count = variations.count()
    context = {
        'variations': variations,
        'variations_count': variations_count,
    }

    return render(request, 'store/store.html', context)
