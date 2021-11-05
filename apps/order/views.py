from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from apps.store.models import Size
from django.shortcuts import render, redirect
from apps.cart.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import datetime
import json


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product = OrderProduct()

        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id

        order_product.variation = item.variation
        order_product.size = item.size

        order_product.quantity = item.quantity
        order_product.product_price = item.variation.price

        order_product.ordered = True

        order_product.save()

        # cart_item = CartItem.objects.get(id=item.id)
        # product_variations = cart_item.variations.all()
        # order_product = OrderProduct.objects.get(id=order_product.id)
        # order_product.variations.set(product_variations)
        # order_product.save()

        # TODO Size quantity
        size = Size.objects.get(id=item.size.id)
        print(size)

        # size.quantity -= item.quantity
        # size.save()

    CartItem.objects.filter(user=request.user).delete()

    try:
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
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
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)

    for cart_item in cart_items:
        total += (cart_item.variation.price * cart_item.quantity)
        quantity += cart_item.quantity

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()

            data.user = current_user
            data.first_name = current_user.first_name
            data.last_name = current_user.last_name

            data.email = current_user.email
            data.phone = current_user.phone_number

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

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

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

    try:
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
    except {Payment.DoesNotExist, Order.DoesNotExist}:
        return redirect('homepage')
