"""
All of the navigation views for the admin pages.
"""
from django.shortcuts import redirect, HttpResponse
from django.views import generic
from restocking.forms import ProductFinderForm

from restocking.models import Product, Transaction, TransactionItem, User

class AdminIndexView(generic.ListView):
    """
    Home page for admin for application
    """
    template_name = 'administration/index.html'

    def get_queryset(self):
        return None

class ProductFinderView(generic.FormView):
    """
    Admin tool to find products
    """
    template_name = 'administration/product_finder.html'
    form_class = ProductFinderForm

    def form_valid(self, form):
        self.request.session['form'] = form.cleaned_data
        return redirect('restocking:product_finder_results')

class ProductFinderResults(generic.ListView):
    """
    Retrieves and displays the results from a product finder query
    """
    model = Product
    template_name = 'administration/show_product_finder_results.html'
    context_object_name = 'results'

    def get_queryset(self):
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

        #Queries are lazy so this will not search for all products initially.
        query = Product.objects.all()

        for field_filter, field, query_type in tuples_list:
            if form[field_filter] is False:
                query = query.filter(**{field + '__' + query_type: form[field]})

        return query

class TransactionIndex(generic.ListView):
    """
    Simple interface to either create a single transaction, or bulk transactions
    """

    template_name = 'administration/transactions/transactions.html'

    def get_queryset(self):
        return None

class TransactionProductFinderView(generic.FormView):
    """
    Admin tool to find products for transactions
    """
    template_name = 'administration/transactions/product_finder.html'
    form_class = ProductFinderForm

    def form_valid(self, form):
        self.request.session['form'] = form.cleaned_data
        return redirect('restocking:transaction_product_finder_results')

class TransactionProductFinderResults(generic.ListView):
    """
    Retrieves and displays the results from a product finder query
    """
    model = Product
    template_name = 'administration/transactions/show_product_finder_results.html'
    context_object_name = 'results'

    def get_queryset(self):
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

        #Queries are lazy so this will not search for all products initially.
        query = Product.objects.all()

        for field_filter, field, query_type in tuples_list:
            if form[field_filter] is False:
                query = query.filter(**{field + '__' + query_type: form[field]})

        return query

def process_transaction(request):
    """
    Process a transaction
    """

    print(request.POST.getlist('checked'))
    transaction = Transaction.objects.create(user=User.objects.get(id=1))
    for product_id in request.POST.getlist('checked'):
        TransactionItem.objects.create(
            quantity=request.POST.get('val ' + product_id),
            product=Product.objects.get(id=product_id),
            transaction=transaction
        )

    return HttpResponse('Success!')
