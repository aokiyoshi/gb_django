def menu_list(request):
    return { 
        'menu': {
            'index': 'Главная',
            'products': 'Продукты',
            'contacts': 'Контакты',
            }
    }