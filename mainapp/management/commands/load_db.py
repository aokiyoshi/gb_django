import json
from unicodedata import name

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from mainapp.models import ProductCategory, Product
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(settings.DATA_ROOT / 'categories.json', 'r', encoding='utf-8') as file:
            categories = json.load(file)
            for category_data in categories:
                try:
                    ProductCategory(**category_data).save()
                except IntegrityError:
                    pass

        with open(settings.DATA_ROOT / 'products.json', 'r', encoding='utf-8') as file:
            products = json.load(file)
            for product_data in products:
                product_data['category'] = ProductCategory.objects.get(
                    name=product_data['category'])
                Product(**product_data).save()

        user = get_user_model()
        if not user.objects.filter(username='admin'):
            get_user_model().objects.create_superuser(
                username='admin', password='admin111')
