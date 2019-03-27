"""
Contains views regarding management navigation
"""
import os

from django.shortcuts import redirect, HttpResponseRedirect, HttpResponse
from django.views import generic
from django.core.mail import send_mail

from restocking.models import Order, OrderItem, Product
from restocking.processing import OrderProcessing

class ManagerIndexView(generic.ListView):
    """
    Home page for manager for application
    """
    template_name = 'manager/index.html'

    def get_queryset(self):
        return None

class AskProcessDelivery(generic.ListView):
    """
    Gives the manager delivery options
    """
    template_name = 'manager/ask_process_delivery.html'
    context_object_name = 'deliveries'

    def get_queryset(self):
        return Order.objects.filter(delivery_processed__exact=False)

class ResultsProcessDelivery(generic.ListView):
    """
    Displays the delivery queried with the ability to process it.
    """
    template_name = 'manager/results_process_delivery.html'
    context_object_name = 'delivery'

    def get_queryset(self):
        order_id = Order.objects.get(delivery_date__exact=self.kwargs['delivery']).id
        return OrderItem.objects.filter(order__exact=order_id).order_by('product__department', 'product__name')

def process_delivery(request, delivery_date):
    """
    Finalises and processes the delivery. Sends an email to the 'warehouse manager'
    """

    #Update stock levels
    order = Order.objects.get(delivery_date__exact=delivery_date)
    order.delivery_processed = True
    order.save()

    order_items = OrderItem.objects.filter(order__exact=order.id)

    for item in order_items.iterator():
        product = Product.objects.get(id__exact=item.product.id)
        product.stock_quantity += item.processed
        product.save()

    #Send email
    order_items_readable = []
    for item in order_items.iterator():
        order_items_readable.append(str(item))

    print(send_mail(
        subject='Delivery ' + str(order.delivery_date),
        message='Dear Manager,\n\nA delivery has been processed.\n\n' + '\n'.join(str(p) for p in order_items_readable) + '\n\nRegards,\nStore Manager',
        from_email=open(os.getcwd() + '/dsp/email_user.txt', 'r').read(),
        recipient_list=[open(os.getcwd() + '/dsp/email_user.txt', 'r').read()],
        fail_silently=False,
    ))

    return redirect('/restocking/manager')

class CreateOrder(generic.ListView):
    """
    Shows a generated order from transactions.
    """
    template_name = 'manager/show_order.html'
    context_object_name = 'order'

    def get_queryset(self):
        order = OrderProcessing().create_order()
        if order is None:
            return HttpResponse("Error")
        else:
            return order