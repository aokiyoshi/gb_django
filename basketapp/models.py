from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property


class BasketManager(models.Manager):
    def quantity(self):
        return sum([item.quantity for item in self.all()])

    def sum(self):
        return sum([item.product.price * item.quantity for item in self.all()])


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(
        verbose_name='время', auto_now_add=True)

    objects = BasketManager()

    @cached_property
    def product_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product} - {self.quantity} шт'

    def get_basket(self, *args, **kwargs):
        return {
            'quantity': self.quantity,
            'sum': self.objects.sum(),
        }


