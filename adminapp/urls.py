import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [\
     path('users/', adminapp.users, name='users'),
     path('users/create/', adminapp.user_create, name='user_create'),
     path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),

     path('users/activate/<int:pk>/', adminapp.user_act_deact, name='user_activate'),
     path('users/deactivate/<int:pk>/', adminapp.user_act_deact, name='user_deactivate'),

     path('categories/create/', adminapp.category_create, name='category_create'),
     path('categories/', adminapp.categories, name='categories'),
     path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),

     path('categories/activate/<int:pk>/', adminapp.category_act_deact, name='category_activate'),
     path('categories/deactivate/<int:pk>/', adminapp.category_act_deact, name='category_deactivate'),

     path('products/create/category/<int:pk>/', adminapp.product_create,
          name='product_create'),
     path('products/read/category/<int:pk>/', adminapp.products,
          name='products'),
     path('products/read/<int:pk>/', adminapp.product_read, name='product_read'),
     path('products/update/<int:pk>/', adminapp.product_update,
          name='product_update'),
     path('products/delete/<int:pk>/', adminapp.product_delete,
          name='product_delete'),
]
