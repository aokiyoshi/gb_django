from django.shortcuts import render
from django.urls import reverse
from mainapp.models import Product, ProductCategory
from random import choice


MENU_LIST = {
    'index': 'Главная',
    'products': 'Продукты',
    'contacts': 'Контакты',
}

INDEX_SLIDER_LIST = [
    {
        'toptitle': 'Тенденции',
        'title': 'удобные стулья',
        'description': 'НОВЫЙ уровень комфорта. Отличные характеристики.',
        'button_text': 'заказать',
        'image': 'img/slider.jpg'
    },
    {
        'toptitle': 'Наш выбор',
        'title': 'Светильники для дома',
        'description': 'Минималистичный дизайн. Высокая надежность',
        'button_text': 'заказать',
        'image': 'img/slider-hotdeal.jpg'
    },
    {
        'toptitle': 'Лучшая статья',
        'title': 'Как выбрать диван для гостинной',
        'description': 'Мнение экспертов в области',
        'button_text': 'читать',
        'image': 'img/slider_art.jpg'
    }
]

# This is page with products and hot product on top 
def products(request):
    products = Product.objects.all()[:]
    categories = ProductCategory.objects.filter(is_active=True)[:]
    hot_product = choice(products)
    return render(
        request,
        'mainapp/products.html',
        context = {
            'menu': MENU_LIST,
            'products': products,
            'hot': hot_product,
            'categories': categories
        } 
    )

# View for product page
def product(request, product_id):
    if Product.objects.filter(pk=product_id):
        product = Product.objects.filter(id=product_id)[0]
        categories = ProductCategory.objects.filter(is_active=True)[:]
        return render(
            request,
            'mainapp/product_page.html',
            context = {
                'menu': MENU_LIST,
                'products': products,
                'categories': categories,
                'product': product,
            } 
        )

def index(request, slide_number=1):
    return render(
        request,
        'mainapp/index.html',
        context = {
            'menu': MENU_LIST,
            'slider_content': INDEX_SLIDER_LIST[slide_number]
        } 
    )

def contacts(request):
    return render(
        request,
        'mainapp/contact.html',
        context = {
            'menu': MENU_LIST
        } 
    )

def category(request, category_id):
    if ProductCategory.objects.filter(id=category_id):
        products = Product.objects.filter(category=category_id)
        hot_product = choice(products)
        categories = ProductCategory.objects.filter(is_active=True)[:]
        return render(
            request,
            'mainapp/products.html',
            context = {
                'menu': MENU_LIST,
                'products': products,
                'hot': hot_product,
                'categories': categories,
                'category_name': ProductCategory.objects.filter(pk=category_id).all()[0]
            } 
        )