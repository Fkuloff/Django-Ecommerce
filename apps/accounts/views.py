import requests
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from apps.celeryapp.tasks import send_email_task
from apps.order.models import Order, OrderProduct
from .forms import RegistrationForm, UserForm
from .models import Account


def register(request):
    if request.method == "POST":

        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password,
            )
            # user.phone_number = phone_number
            user.save()

            # User activation
            current_site = get_current_site(request)
            mail_subject = 'Пожалуйста, активируйте свою учетную запись'
            message = render_to_string('email/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_email_task.delay(mail_subject, message, email)

            messages.success(request, 'Мы отправили вам письмо с подтверждением.')
            return redirect('/accounts/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Вы вошли в систему')

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print('query ->', query)
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Неверные логин или пароль')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш аккаунт активирован!')

        return redirect('login')
    else:
        messages.error(request, 'Недействительная ссылка для активации.')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    order = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = order.count()

    context = {
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password
            current_site = get_current_site(request)
            mail_subject = 'Сбросить пароль'
            message = render_to_string('email/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_email_task.delay(mail_subject, message, email)

            messages.success(request, 'Письмо для сброса пароля было отправлено на ваш адрес электронной почты.')
            return redirect('login')

        else:
            messages.error(request, 'Аккаунт не существует!')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Сбросить пароль')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Срок действия этой ссылки истек')
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Сброс пароля выполнен успешно')
            return redirect('login')
        else:
            messages.error(request, 'Пароль не совпадает')
            return redirect('resetPassword')
    return render(request, 'accounts/reset_password.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш профиль был обновлен')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
    context = {
        'user_form': user_form,
    }

    return render(request, 'dashboard/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)

        success = user.check_password(current_password)
        if new_password == confirm_password:
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Пароль успешно обновлен')
                return redirect('change_password')
            else:
                messages.error(request, 'Введите действующий пароль')
                return redirect('change_password')
        else:
            messages.error(request, 'Пароль не подходит!')
            return redirect('change_password')

    return render(request, 'dashboard/change_password.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    order_products = OrderProduct.objects.filter(order__order_number=order_id)

    order = Order.objects.get(order_number=order_id)

    subtotal = 0
    for i in order_products:
        subtotal += i.product_price * i.quantity

    context = {
        'order_products': order_products,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)
