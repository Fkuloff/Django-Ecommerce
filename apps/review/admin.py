from django.contrib import admin

from .models import ReviewRating


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'subject')


admin.site.register(ReviewRating, ReviewRatingAdmin)
