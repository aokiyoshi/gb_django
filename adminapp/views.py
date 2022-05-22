from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse
from mainapp.models import Product, ProductCategory

from adminapp.forms import ProductCategoryEditForm, ShopUserAdminEditForm, ProductCategoryCreateForm


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def users(request):
    title = 'админка/пользователи'\

    users_list = ShopUser.objects.all().order_by(
        '-is_active', '-is_superuser', '-is_staff', 'username')
    content = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {'title': title, 'update_form': user_form}

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(
            request.POST, request.FILES, instance=edit_user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(
                reverse('admin:user_update', args=[edit_user.pk])
            )
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {'title': title, 'update_form': edit_form}

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def user_act_deact(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    user.is_active = not user.is_active
    user.save()

    return HttpResponseRedirect(reverse('admin:users'))


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }
    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def category_create(request):
    title = 'категории/создание'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)

        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm()

    content = {'title': title, 'update_form': category_form}

    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def category_update(request, pk):
    title = 'категории/редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(
            request.POST, request.FILES, instance=edit_category)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(
                reverse('admin:category_update', args=[edit_category.pk])
            )
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    content = {'title': title, 'update_form': edit_form}

    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def category_act_deact(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    category.is_active = not category.is_active
    category.save()

    return HttpResponseRedirect(reverse('admin:categories'))


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def products(request, pk):
    title = 'админка/продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')
    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }
    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def product_create(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def product_read(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def product_update(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def product_delete(request, pk):
    pass
