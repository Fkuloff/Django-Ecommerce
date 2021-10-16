from django.db.models import Q
from django.shortcuts import render
from .models import Product, ProductGallery, Variation, Size, Specification
from django.core.paginator import Paginator
from apps.order.models import OrderProduct
from apps.review.models import ReviewRating


def store(request, category_slug=None):
    categories = None
    products = None

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
    products = Product.objects.filter(is_available=True).order_by('-id')
    product_count = products.count()

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, product_slug, variation_vendor_code):
    try:
        single_product = Product.objects.get(slug=product_slug)
        specifications = Specification.objects.filter(product=single_product)

        variation = Variation.objects.get(vendor_code=variation_vendor_code)

        product_gallery = ProductGallery.objects.filter(variation=variation)
        sizes = Size.objects.filter(variation=variation)

        # in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),
        #                                   product=single_product).exists()  # True/False
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    # get reviews

    reviews = ReviewRating.objects.filter(variation=variation, status=True)


    context = {
        'single_product': single_product,
        # 'in_cart': in_cart,
        'variation': variation,
        'sizes': sizes,
        'order_product': order_product,
        'reviews': reviews,
        'specifications': specifications,
        'product_gallery': product_gallery,
    }

    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)
