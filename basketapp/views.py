from django.views import View
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from mainapp.models import Product

from basketapp.models import Basket
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class BasketView(LoginRequiredMixin, ListView):
    title = 'Корзина'
    model = Basket
    template_name = 'basketapp/basket.html'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)
    

class BasketAdd(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])

        quantity = self.kwargs.get('quantity', 1)
        basket = Basket.objects.filter(user=self.request.user, product=product).first()

        if not basket:
            basket = Basket(user=self.request.user, product=product)

        basket.quantity += quantity
        basket.save()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        

class BasketRemoveAll(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        baskets = Basket.objects.filter(user=self.request.user)
        baskets.delete()
        return HttpResponseRedirect(reverse('basket:view'))


class BasketRemove(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        basket = get_object_or_404(Basket, pk=self.kwargs['pk'])
        basket.delete()
        return JsonResponse({'result': ''})


class BasketEdit(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        basket = get_object_or_404(Basket, pk=self.kwargs['pk'])
        quantity = self.kwargs['quantity']

        if quantity == 0:
            basket.delete()
            result = ''

        else:
            if quantity <= basket.product.quantity:
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
    basket = Basket.objects.filter(user=self.request.user)
    bsum = basket.sum()
    bquantity = basket.quantity()
    total = render_to_string(
            'basketapp/includes/basket_total_fetch.html', 
            request=request, 
            context={
                'user': user,
                'sum': bsum,
                'quantity': bquantity,
                }
            )
    return JsonResponse({'total': total})
