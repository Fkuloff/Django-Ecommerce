from django.db import models
from apps.store.models import Product, Variation
from apps.accounts.models import Account


class Cart(models.Model):
    cart_id = models.CharField(max_length=256, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)

    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.variation.price * self.quantity

    def __unicode__(self):
        return self.variation
