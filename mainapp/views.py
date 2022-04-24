from django.shortcuts import render
from django.urls import reverse


MENU_LIST = {
    'index': 'Главная',
    'products': 'Продукты',
    'contacts': 'Контакты'
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
    return render(
        request,
        'mainapp/products.html',
        context = {
            'menu': MENU_LIST,
            'products': [
                {
                    'name': 'Люстра', 
                    'description': 'Отличныый дизанй', 
                    'image': 'product-11.jpg',
                },
                {
                    'name': 'Красивый стул', 
                    'description': 'Минималистичный дизайн', 
                    'image': 'product-21.jpg'
                },
                {
                    'name': 'Светильник Черный', 
                    'description': 'Отличный дизайн', 
                    'image': 'product-31.jpg'
                },
                {
                    'name': 'Еще один продукт', 
                    'description': 'Удобство и комфорт', 
                    'image': 'product-41.jpg'
                },
                {
                    'name': 'Еще один продукт', 
                    'description': 'Удобство и комфорт', 
                    'image': 'product-51.jpg'
                },

            ]
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