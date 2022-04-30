from django.shortcuts import render
from django.urls import reverse
from mainapp.models import Product, ProductCategory

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

def products(request):
    products = Product.objects.all()[:]
    categories = ProductCategory.objects.all()[:]
    return render(
        request,
        'mainapp/products.html',
        context = {
            'menu': MENU_LIST,
            'products': products,
            'categories': categories
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