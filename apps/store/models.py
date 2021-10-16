from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
from apps.category.models import Category
from apps.accounts.models import Account
from apps.review.models import ReviewRating


class Product(models.Model):
    product_name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    composition = models.TextField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    seller = models.CharField(max_length=64, blank=True)

    is_available = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        variation_vendor_code = Variation.objects.filter(product_id=self.pk)[0]
        return reverse('product_detail',
                       kwargs={"variation_vendor_code": variation_vendor_code, 'product_slug': self.slug})





    class Meta:
        verbose_name = 'Product'


class Specification(models.Model):
    title = models.CharField(max_length=64)
    value = models.CharField(max_length=64)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Variation(models.Model):
    vendor_code = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=64)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.vendor_code

    def average_review(self):
        reviews = ReviewRating.objects.filter(variation=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = ReviewRating.objects.filter(variation=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class Size(models.Model):
    size_number = models.CharField(max_length=4)
    quantity = models.PositiveIntegerField()
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)

    def __str__(self):
        return self.size_number


class ProductGallery(models.Model):
    variation = models.ForeignKey(Variation, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.variation.vendor_code

    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product gallery'
