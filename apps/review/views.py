from django.contrib import messages
from django.shortcuts import redirect

from .forms import ReviewForm
from .models import ReviewRating


def submit_review(request, single_product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product_id=single_product_id)
            form = ReviewForm(request.POST, instance=reviews)  # instance update review
            form.save()
            messages.success(request, 'Thank you for review!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']

                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = single_product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you for review!')
                return redirect(url)
