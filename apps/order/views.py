import datetime
import json

from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from apps.cart.models import CartItem, Cart
from apps.store.models import Size
from apps.cart.views import _cart_id
from .forms import OrderForm
from .models import Order, Payment, OrderProduct


def payments(request):
    body = json.loads(request.body)

    if request.user.is_authenticated:
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
        payment = Payment(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=order.order_total,
            status=body['status'],
        )
        payment.save()
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        print(cart)
        order = Order.objects.get(cart=cart, is_ordered=False, order_number=body['orderID'])
        payment = Payment(
            cart=cart,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=order.order_total,
            status=body['status'],
        )
        payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(cart=cart)

    for item in cart_items:
        order_product = OrderProduct()

        order_product.order_id = order.id
        order_product.payment = payment

        if request.user.is_authenticated:
            order_product.user_id = request.user.id
        else:
            order_product.cart = cart

        order_product.variation = item.variation
        order_product.size = item.size
        order_product.quantity = item.quantity
        order_product.product_price = item.variation.price
        order_product.ordered = True

        order_product.save()

        # TODO Size quantity
        size = Size.objects.get(id=item.size.id)

        # size.quantity -= item.quantity
        # size.save()

    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        CartItem.objects.filter(cart=cart).delete()

    try:
        mail_subject = 'Thank you for your order!'
        message = render_to_string('email/order_received_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
    except Exception as e:
        print(e)

    data = {
        'order_number': order.order_number,
        'payment_id': payment.payment_id,
    }

    return JsonResponse(data)


def place_order(request, total=0, quantity=0):
    if request.user.is_authenticated:
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)

    for cart_item in cart_items:
        total += (cart_item.variation.price * cart_item.quantity)
        quantity += cart_item.quantity

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()

            if request.user.is_authenticated:
                data.user = current_user
                data.first_name = current_user.first_name
                data.last_name = current_user.last_name
                data.email = current_user.email
                data.phone = current_user.phone_number
            else:
                data.cart = cart
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.email = form.cleaned_data['email']
                data.phone = form.cleaned_data['phone']

            data.street = form.cleaned_data['street']
            data.house = form.cleaned_data['house']
            data.entrance = form.cleaned_data['entrance']
            data.floor = form.cleaned_data['floor']

            # data.order_note = form.cleaned_data['order_note']

            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')

            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%y%m%d')
            order_number = current_date + str(data.id)

            data.order_number = order_number

            data.save()

            if request.user.is_authenticated:
                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            else:
                order = Order.objects.get(id=data.id, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('cart')


def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')

    order = Order.objects.get(order_number=order_number, is_ordered=True)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)

    subtotal = 0
    for i in ordered_products:
        subtotal += i.product_price * i.quantity

    payment = Payment.objects.get(payment_id=payment_id)

    context = {
        'order': order,
        'ordered_products': ordered_products,
        'order_number': order.order_number,
        'transID': payment.payment_id,
        'payment': payment,
        'subtotal': subtotal,
    }

    return render(request, 'orders/order_complete.html', context)
    # except {Payment.DoesNotExist, Order.DoesNotExist}:
    #     return redirect('homepage')
