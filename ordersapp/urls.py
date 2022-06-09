from django.shortcuts import render
from django.urls import path
import ordersapp.views as ordersapp

app_name = "ordersapp"

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='orders_list'),
    path('create/', ordersapp.create_order, name='order_create'),
    path('order/<int:pk>', ordersapp.OrderEdit.as_view(), name='order_edit'),
    path('pay/<int:pk>', ordersapp.OrderPay.as_view(), name='order_pay'),
    path('cansel/<int:pk>', ordersapp.OrderCansel.as_view(), name='order_cansel'),
#     path('update/<int:pk>',
#          ordersapp.OrderItemsUpdate.as_view(),
#          name='order_update'),
#     path('delete/<int:pk>',
#          ordersapp.OrderDelete.as_view(),
#          name='order_delete'),
]