from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse
from mainapp.models import Product

from basketapp.models import Basket
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required(login_url='/auth/login/')
def basket(request):
    basket = Basket.objects.filter(user=request.user)
    return render(
        request,
        'basketapp/basket.html',
        context={
            'basket': basket
        }
    )


@login_required(login_url='/auth/login/')
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/auth/login/')
def basket_remove_all(request):
    baskets = Basket.objects.filter(user=request.user)
    baskets.delete()
    return HttpResponseRedirect(reverse('basket:view'))


@login_required(login_url='/auth/login/')
def basket_remove(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return JsonResponse({'result': ''})


@login_required(login_url='/auth/login/')
def basket_edit(request, pk, quantity):

    basket = get_object_or_404(Basket, pk=pk)

    if quantity == 0:
        basket.delete()
        result = ''

    else:
        basket.quantity = quantity
        result = render_to_string(
            'basketapp/includes/basket_element.html',
            context={
                'basket_element': basket
            }
        )
    basket.save()
    return JsonResponse({'result': result})

@login_required
def basket_total(request):
    user = request.user
    total = render_to_string('basketapp/includes/basket_total_fetch.html', request=request, context={'user': user})
    return JsonResponse({'total': total})