from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.BasketView.as_view(), name='view'),
    path('add/<int:pk>/', basketapp.BasketAdd.as_view(), name='add'),
    path('remove/<int:pk>/', basketapp.BasketRemove.as_view(), name='remove'),
    path('remove/all/', basketapp.BasketRemoveAll.as_view(), name='remove_all'),
    path('edit/<int:pk>/<int:quantity>/', basketapp.BasketEdit.as_view(), name='edit'),
    path('basket_total/', basketapp.basket_total, name='basket_total'),
]
