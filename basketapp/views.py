from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse
from mainapp.models import Product

from basketapp.models import Basket


def basket(request):
    basket = Basket.objects.filter(user=request.user)
    return render(
        request,
        'basketapp/basket.html',
        context={
            'basket': basket
        }
    )


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return HttpResponseRedirect(reverse('basket:view'))


def basket_remove_all(request):
    baskets = Basket.objects.filter(user=request.user)
    baskets.delete()
    return HttpResponseRedirect(reverse('basket:view'))
