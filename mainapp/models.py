from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import connection


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)
    
    def __str__(self):
        return f'{self.id}: {self.name}'

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', default='default.jpg')
    short_desc = models.CharField(verbose_name='краткое описание продукта',
                                  max_length=60, blank=True)
    description = models.TextField(
        verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8,
                                decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе',
                                           default=0)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'
    
    def get_items(self):
        return []

def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(post_save, sender=ProductCategory)
def update_product(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)




