from basketapp.models import Basket
from django.db import transaction
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView, UpdateView
from django.views.generic.base import ContextMixin
from requests import request

from ordersapp.models import Order, OrderItem

from .forms import OrderFormSet


class OrderList(ListView):
    model = Order
    template_name = 'ordersapp/order_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class OrderEdit(UpdateView):
    template_name = "ordersapp/order_update.html"
    model = Order
    success_url = reverse_lazy("orders:orders_list")
    fields = ()

    def get_context_data(self, **kwargs):
        formset = kwargs.get("formset", OrderFormSet(instance=self.object))
        context = super().get_context_data(**kwargs)
        context["orderitems"] = formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = OrderFormSet(self.request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    @transaction.atomic
    def form_valid(self, form, formset):
        self.object = form.save()
        formset.save()
        return super().form_valid(form)

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset))


class OrderChangeStatus(View):
    status = None

    def get(self, *args, **kwargs):
        print('!')
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        order.status = self.status
        order.save()
        return HttpResponseRedirect(reverse_lazy('orders:orders_list'))


class OrderPay(OrderChangeStatus, View):
    status = Order.PAID


class OrderCansel(OrderChangeStatus, View):
    status = Order.CREATED


def create_order(request):
    user = request.user
    basket = Basket.objects.filter(user=request.user)
    order = Order(user=user)
    order.save()
    for item in basket:
        product = item.product
        if product.quantity >= item.quantity:
            product.quantity -= item.quantity
            order_item = OrderItem(product=product,
                                order=order,
                                quantity=item.quantity)
            order_item.save()
        product.save()
        item.delete()
    return HttpResponseRedirect(reverse('ordersapp:orders_list'))

