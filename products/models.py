from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
class Product(models.Model):
    title = models.CharField(
        verbose_name = 'Title',
        max_length = 255,
    )

    price = MoneyField(
        max_digits=14, 
        decimal_places=0, 
        default_currency='KZT'
    )

    quantity = models.IntegerField(
        verbose_name = 'Quantity',
    )

    created = models.DateTimeField(
        verbose_name = "Created",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Updated",
        auto_now = True,
    )

    class Meta:

        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ('-created',)

    def __str__(self):
        return '%s' % self.pk