from django.contrib import admin

from authapp.models import ShopUser
from basketapp.models import Basket
from .models import ProductCategory, Product

# Register your models here.
admin.site.register(ShopUser)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Basket)
