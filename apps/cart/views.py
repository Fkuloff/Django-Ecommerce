from django.shortcuts import render, redirect, get_object_or_404
from apps.store.models import Product, Variation, Size
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, variation_id):
    variation = Variation.objects.get(id=variation_id)
    current_user = request.user

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                size = Size.objects.get(variation=variation, id=value)
            except:
                pass

    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(variation=variation, size=size, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(variation=variation, size=size, user=current_user)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                variation=variation,
                size=size,
                quantity=1,
                user=current_user,
            )
            cart_item.save()
        return redirect('cart')
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(variation=variation, size=size, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.get(variation=variation, size=size, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                variation=variation,
                size=size,
                quantity=1,
                cart=cart
            )
            cart_item.save()
    return redirect('cart')


def add_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def remove_cart(request, variation_id, cart_item_id):
    variation = get_object_or_404(Variation, id=variation_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(variation=variation, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(variation=variation, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def delete_cart_item(request, variation_id, cart_item_id):
    variation = get_object_or_404(Variation, id=variation_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(variation=variation, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(variation=variation, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.variation.price * cart_item.quantity)
            quantity += cart_item.quantity

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)

