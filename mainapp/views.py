from random import choice
from select import select

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, TemplateView
from django.views.generic.list import ListView

from mainapp.models import Product, ProductCategory

from django.conf import settings
from django.core.cache import cache


INDEX_SLIDER_LIST = [{
    'toptitle': 'Тенденции',
    'title': 'удобные стулья',
    'description': 'НОВЫЙ уровень комфорта. Отличные характеристики.',
    'button_text': 'заказать',
    'image': '/static/img/slider.jpg'
}, {
    'toptitle': 'Наш выбор',
    'title': 'Светильники для дома',
    'description': 'Минималистичный дизайн. Высокая надежность',
    'button_text': 'заказать',
    'image': '/static/img/slider-hotdeal.jpg'
}, {
    'toptitle': 'Лучшая статья',
    'title': 'Как выбрать диван для гостинной',
    'description': 'Мнение экспертов в области',
    'button_text': 'читать',
    'image': '/static/img/slider_art.jpg'
}]


# Products list view for 'All' category
class ProductList(ListView):
    model = Product
    template_name = 'mainapp/products.html'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)[:]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.filter(
            is_active=True)[:]
        context["hot"] = choice(self.object_list)
        return context


# View for product page
class ProductView(DetailView):
    model = Product
    template_name = 'mainapp/product_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.filter(
            is_active=True)[:]
        return context


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slide_number = context.get('slide_number', 1)
        context['slider_content'] = INDEX_SLIDER_LIST
        context['slider_length'] = len(INDEX_SLIDER_LIST)
        return context


class ContactsView(TemplateView):
    template_name = 'mainapp/contact.html'


class CategoryList(ListView):
    model = Product
    template_name = 'mainapp/products.html'

    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']
        
        if not settings.LOW_CACHE:
            return self.model.objects.filter(is_active=True, category=pk)[:]

        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = self.model.objects.filter(is_active=True, category=pk)[:]
        
        return category


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.filter(
            is_active=True)[:]
        if self.object_list:
            context["hot"] = choice(self.object_list)
        context['category_name'] = ProductCategory.objects.filter(
            pk=self.kwargs['pk']).all()[0]
        return context
