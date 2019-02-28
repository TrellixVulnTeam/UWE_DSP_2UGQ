# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.views import generic
from .models import Product, NfcUnit, Order, OrderItem, StockKeepingUnit
from .forms import ProductFinderForm
from rest_framework import generics
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer

import random
import json
import os

import processing.nfc_processing as nfc_processing

# Create your views here.
class IndexView(generic.ListView):
    """
    Home page for admin for application
    """
    template_name = 'admin/restocking/index.html'

    def get_queryset(self):
        return None

def skus(request):
    """
    Creates skus
    """
    path = os.getcwd()
    with open(path + '/restocking/data/stock_keeping_units.json') as data_file:
        sku_data = json.load(data_file)

    for i in range (sku_data['department']['mens']['quantity']):
        StockKeepingUnit.objects.create()

    for i in range (sku_data['department']['ladies']['quantity']):
        StockKeepingUnit.objects.create()

    for i in range (sku_data['department']['childrens']['quantity']):
        StockKeepingUnit.objects.create()


def add_quantities(request):
    """
    Test assigning random(ish) quantities to each product.
    """

    path = os.getcwd()
    with open(path + '/restocking/data/initial_product_levels.json') as data_file:
        quantity_data = json.load(data_file)

    product_set = Product.objects.all()

    for product in product_set:
        if product.size in quantity_data['department'][product.department]['size_data']['common']:
            size_category = 'common'
        else:
            size_category = 'uncommon'

        if '.5' in str(product.size):
            size_half = 'half'
        else:
            size_half = 'whole'

        quantity = quantity_data['department'][product.department]['code'][product.product_code]['size'][size_category][size_half]
        product.stock_quantity = quantity + random.randint((quantity/2 * -1), (quantity/2))
        product.save()

    return HttpResponse('Success')

def add_data(request):
    """Creates random data from a file"""
    _colour_pop_chance = 50
    _fitting_pop_chance = 75
    products = []
    def randint_x(n_1, n_2):
        """Returns a random number within the given range (exclusive)"""
        return random.randint(n_1, n_2-1)

    path = os.getcwd()
    with open(path + '/restocking/product_metadata.json') as data_file:
        product_md = json.load(data_file)

    name_list = []#list to prevent duplicate names
    for department in product_md:
        for code in product_md[department]['codes']:
            for shoe in range(product_md[department]['codes'][code]['quantity']):
                #Name
                duplicate = True
                while duplicate:
                    primary_name = product_md[department]['codes'][code]['names'][randint_x(0, len(product_md[department]['codes'][code]['names']))]
                    secondary_name = product_md[department]['secondary'][randint_x(0, len(product_md[department]['secondary']))]
                    name = primary_name+" "+secondary_name
                    if name not in name_list:
                        name_list.append(name)
                        duplicate = False
                #Size
                sizes = []
                if department == 'childrens':
                    for size in range(0, len(product_md[department]['codes'][code]['sizes'])):
                        sizes.append(product_md[department]['codes'][code]['sizes'][size])
                else:
                    for size in range(0, len(product_md[department]['codes'][code]['sizes']), random.randint(1, 2)):
                        sizes.append(product_md[department]['codes'][code]['sizes'][size])
                #Fitting
                fittings = list(product_md[department]['codes'][code]['fittings'])
                if department == 'childrens':
                    if product_md[department]['codes'][code]['type'] == 'shoe' and random.randint(0, 1) == 1:
                        fittings.pop()
                        fittings.pop()
                else:
                    for x in range(0, len(fittings)-1):
                        if random.randint(0, 100) <= _fitting_pop_chance:
                            fittings.pop()
                #Colour
                colours = list(product_md[department]['codes'][code]['colours'])
                for x in range(len(colours)-1):
                    if random.randint(0, 100) <= _colour_pop_chance:
                        colours.pop()
                #Price
                price = product_md[department]['codes'][code]['prices'][randint_x(0, len(product_md[department]['codes'][code]['prices']))]
                product_type = product_md[department]['codes'][code]['type']
                product_code = code
                department = department

                for size in sizes:
                    for fitting in fittings:
                        for colour in colours:
                            product = Product(
                                name=name,
                                size=size,
                                fitting=fitting,
                                colour=colour,
                                price=price,
                                product_type=product_type,
                                product_code=product_code,
                                department=department
                            )
                            product.save()

    return HttpResponse("DONE")

class ProductFinderView(generic.FormView):
    """
    Admin tool to find products
    """
    template_name = 'admin/restocking/product_finder.html'
    form_class = ProductFinderForm

    def form_valid(self, form):
        self.request.session['form'] = form.cleaned_data
        if 'device' in self.kwargs:
            self.request.session['device'] = self.kwargs['device']

        if self.request.resolver_match.url_name == 'product_finder':
            return redirect('restocking:product_finder_results')
        else:
            return redirect('restocking:tag_encoder_pick_product')


class ProductFinderResults(generic.ListView):
    """
    Retrieves and displays the results from a product finder query
    """
    model = Product
    template_name = 'admin/restocking/show_product_finder_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        #Queries are lazy so this will not search for all products initially.
        form = self.request.session['form']

        tuples_list = (
            ['filter_name', 'name', 'icontains'],
            ['filter_size', 'size', 'exact'],
            ['filter_colour', 'colour', 'exact'],
            ['filter_fitting', 'fitting', 'exact'],
            ['filter_price', 'price', 'contains'],
            ['filter_sale', 'sale', 'exact'],
            ['filter_product_type', 'product_type', 'exact'],
            ['filter_product_code', 'product_code', 'exact'],
            ['filter_department', 'department', 'exact']
        )

        query = Product.objects.all()

        for field_filter, field, query_type in tuples_list:
            if form[field_filter] is False:
                query = query.filter(**{field + '__' + query_type: form[field]})

        return query

class NfcIndex(generic.ListView):
    """
    Provides interface for accessing NFC functionalities.
    """

    template_name = 'admin/restocking/nfc_index.html'

    def get_queryset(self):
        return None

def find_nfc_devices(request):
    if nfc_processing.nfc_find_devices():
        return HttpResponse("Success!")
    else:
        return HttpResponse('Failure! Check if there are NFC devices plugged in.')

class NfcDevicePicker(generic.ListView):
    """
    Provides list of NFC devices to perform various tasks with.
    """

    context_object_name = 'devices'
    template_name = 'admin/restocking/nfc_device_picker.html'

    def get_queryset(self):
        return NfcUnit.objects.all()

def nfc_identify(request, device):
    identify_results = nfc_processing.nfc_identify_tag(device)
    if identify_results is not None:
        return HttpResponse("<p>Product ID is: " + identify_results + '</p>' + "<p>Product Name is: " + Product.objects.get(id__exact=identify_results).__str__() + '</p>')
    else:
        return HttpResponse('Failure!')

def nfc_encode(request):
    if nfc_processing.nfc_encode_tag(request.session['device'], request.POST.get('radios', '')):
        return HttpResponse("Success!")
    else:
        return HttpResponse("Failure!")

class DetailsViewOrder(generics.RetrieveUpdateAPIView):
    """Handles GET, PUT and DELETE for orders"""
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

class DetailsViewOrderByDate(generics.RetrieveUpdateAPIView):
    """Handles GET, PUT and DELETE for products by date"""
    serializer_class = OrderSerializer
    lookup_field = 'delivery_date'

    def get_queryset(self):
        delivery_date = self.kwargs['delivery_date']
        return Order.objects.filter(delivery_date__exact=delivery_date)

class DetailsViewOrderByDateFilterProduct(generics.RetrieveUpdateAPIView):
    """Handles GET, PUT and DELETE for products by date and by product id"""
    serializer_class = OrderSerializer
    lookup_field = 'delivery_date'

    def get_queryset(self):
        delivery_date = self.kwargs['delivery_date']
        product = self.kwargs['product_id']
        if product is not None:
            try:
                query = Order.objects.filter(
                    delivery_date__exact=delivery_date, 
                    id__exact=OrderItem.objects.get(product__exact=product).order.id
                )
            except Exception as e:
                if e.message == 'OrderItem matching query does not exist.':
                    return None
                else:
                    raise e

            return query 

class CreateOrderItemView(generics.ListCreateAPIView):
    """Handles POST"""
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.all()

    def perform_create(self, serializer):
        OrderItem(
            order=Order.objects.get(id__exact=serializer.data['order']),
            quantity=serializer.data['quantity'],
            processed=serializer.data['processed'],
            product=Product.objects.get(id__exact=serializer['product']['id'].value)
        ).save()

class DetailsViewProduct(generics.RetrieveUpdateAPIView):
    """Handles GET, PUT and DELETE for products"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

