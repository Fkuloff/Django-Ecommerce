from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderProductInLine(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'created_at', 'status', 'is_ordered')
    list_filter = ('status', 'is_ordered')
    # search_fields = ('order_number', 'user', 'created_at', 'email')
    list_per_page = 20
    inlines = [OrderProductInLine]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'payment_method', 'amount_paid', 'status', 'created_at')


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
