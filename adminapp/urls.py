import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [\
     path('users/', adminapp.UsersListView.as_view(), name='users'),
     path('users/create/', adminapp.UserCreate.as_view(), name='user_create'),
     path('users/update/<int:pk>/', adminapp.UserUpdate.as_view(), name='user_update'),
     path('users/activate/<int:pk>/', adminapp.user_act_deact, name='user_activate'),
     path('users/deactivate/<int:pk>/', adminapp.user_act_deact, name='user_deactivate'),

     path('categories/', adminapp.CategoriesView.as_view(), name='categories'),
     path('categories/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
     path('categories/update/<int:pk>/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
     path('categories/activate/<int:pk>/', adminapp.category_act_deact, name='category_activate'),
     path('categories/deactivate/<int:pk>/', adminapp.category_act_deact, name='category_deactivate'),

     path('products/<int:pk>/', adminapp.ProductsView.as_view(), name='products'),
     path('products/create/category/<int:pk>/', adminapp.ProductCreate.as_view(),
          name='product_create'),
     path('products/update/<int:pk>/', adminapp.ProductUpdate.as_view(),
          name='product_update'),
     path('products/activate/<int:pk>/', adminapp.product_act_deact, name='product_activate'),
     path('products/deactivate/<int:pk>/', adminapp.product_act_deact, name='product_deactivate'),
]
