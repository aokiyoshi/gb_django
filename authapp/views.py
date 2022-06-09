from turtle import title
from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from authapp.forms import (ShopUserEditForm, ShopUserLoginForm,
                           ShopUserRegisterForm)
from authapp.models import ShopUser

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView

from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


class Login(LoginView):
    template_name = 'authapp/login.html'
    form_class = ShopUserLoginForm


class Logout(LogoutView):
    next_page = '/'


class RegisterView(CreateView):
    title = 'регистрация'

    template_name = 'authapp/register.html'

    form_class = ShopUserRegisterForm

    def post(self, request, *args, **kwargs):
        register_form = self.get_form()
        if register_form.is_valid():
            user = register_form.save()
            register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
            else:
                print('ошибка отправки сообщения')
            return HttpResponseRedirect(reverse('auth:login'))


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST,
                                     request.FILES,
                                     instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify',
                          args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
        {settings.DOMAIN_NAME} перейдите по ссылке \
        \n{settings.DOMAIN_NAME}{verify_link}'
        
    return send_mail(title,
                     message,
                     settings.EMAIL_HOST_USER, [user.email],
                     fail_silently=False)

def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'Error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))
