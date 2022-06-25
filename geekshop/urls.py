"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from mainapp.views import ProductList, ProductView, IndexView, ContactsView, CategoryList

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('__debug__/', include('debug_toolbar.urls')),

    path('', include('social_django.urls', namespace='social')),
    
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),

    path('products/', ProductList.as_view(), name='products'),
    path('products/<int:pk>', CategoryList.as_view(), name='category'),
    path('product/<int:pk>', ProductView.as_view(), name='product'),

    path('auth/', include('authapp.urls', namespace='auth')),

    path('basket/', include('basketapp.urls', namespace='basket')),

    path('orders/', include('ordersapp.urls', namespace='orders')),

    path('<int:slide_number>/', IndexView.as_view(), name='index'),
    re_path(r'^favicon\.ico$', favicon_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
