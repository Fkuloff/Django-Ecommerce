from django.contrib import admin

from .models import ReviewRating


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'variation', 'rating', 'subject')


admin.site.register(ReviewRating, ReviewRatingAdmin)
