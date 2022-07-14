from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from mainapp.models import Product, ProductCategory

from ordersapp.models import OrderItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProductCategoryEditForm
from mainapp.models import db_profile_by_type
from django.db import connection
from django.db.models import F

# Mixins
class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


# Users
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    paginate_by = 4


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserCreate(TitleMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('adminapp:users')
    fields = "__all__"
    title = 'пользователи/создание'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserUpdate(UserCreate, UpdateView):
    title = 'пользователи/редактирование'


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def user_act_deact(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    user.is_active = not user.is_active
    user.save()

    return HttpResponseRedirect(reverse('admin:users'))


# Categories
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoriesView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    paginate_by = 4


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryCreateView(TitleMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'
    title = 'категории/создание'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    title = 'категории/редактирование'
    
    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def category_act_deact(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    category.is_active = not category.is_active
    category.save()

    return HttpResponseRedirect(reverse('admin:categories'))


# Product
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductsView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCreate(TitleMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('adminapp:categories')
    fields = "__all__"
    title = 'товары/создание'

    def form_valid(self, form):
        form.cleaned_data['category'] = ProductCategory.objects.filter(
            pk=self.kwargs['pk'])
        return super().form_valid(form)


class ProductUpdate(ProductCreate, UpdateView):
    title = 'товары/редактирование'


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def product_act_deact(request, pk):
    product = get_object_or_404(Product, pk=pk)

    product.is_active = not product.is_active
    product.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class OrderList(ListView):
    model = OrderItem
    template_name = 'adminapp/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.all()
        return context
    

@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def order_send(request, pk):
    order = get_object_or_404(Order, pk=pk)

    order.status = Order.SENT
    order.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class OrderDelete(SuperUserRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('admin:orders')
