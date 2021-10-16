from django.contrib import admin
from .models import *
import admin_thumbnails
import nested_admin


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(nested_admin.NestedTabularInline):
    model = ProductGallery
    extra = 1
    list_display = ''


class SpecificationsInline(nested_admin.NestedTabularInline):
    model = Specification
    extra = 5


class SizesInline(nested_admin.NestedTabularInline):
    model = Size
    extra = 5


class VariationsInline(nested_admin.NestedStackedInline):
    model = Variation
    extra = 1
    inlines = [SizesInline, ProductGalleryInline]


class ProductAdmin(nested_admin.NestedModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [SpecificationsInline, VariationsInline]
    list_display = ('product_name', 'seller', 'created_date', 'is_available')


# class VariationAdmin(admin.ModelAdmin):
#     list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
#     list_editable = ('is_active',)
#     list_filter = ('product', 'variation_category', 'variation_value')


admin.site.register(Product, ProductAdmin)
# admin.site.register(Specification)
# admin.site.register(Variation)
# admin.site.register(Size)
# admin.site.register(ProductGallery)

# admin.site.register(Variation, VariationAdmin)
# admin.site.register(ReviewRating)
# admin.site.register(ProductGallery)
