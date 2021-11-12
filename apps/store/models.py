from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse

from apps.accounts.models import Account
from apps.category.models import Category
from apps.review.models import ReviewRating


class Product(models.Model):
    product_name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    composition = models.TextField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    seller = models.CharField(max_length=64, blank=True)

    main_img = models.ImageField(upload_to='store/products', max_length=255)

    is_available = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

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

    def get_sizes(self):
        sizes = Size.objects.filter(variation=self)
        return sizes

    def get_variation_gallery(self):
        var_gallery = VariationGallery.objects.filter(variation=self).first()
        return var_gallery

    def get_absolute_url(self):
        return reverse('product_detail',
                       kwargs={"variation_vendor_code": self.vendor_code, 'product_slug': self.product.slug})


class Size(models.Model):
    size_number = models.CharField(max_length=4)
    quantity = models.PositiveIntegerField()
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)

    def __str__(self):
        return self.size_number


class VariationGallery(models.Model):
    variation = models.ForeignKey(Variation, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.variation.vendor_code

    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product gallery'
