"""
All of the navigation views for the admin pages.
"""
from django.shortcuts import redirect
from django.views import generic
from restocking.forms import ProductFinderForm

from restocking.models import Product

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
