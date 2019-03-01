"""
Provides the functions behind the admin views.
"""
from django.views import generic
from restocking.models import Product

class ProductFinderResults(generic.ListView):
    """
    Retrieves and displays the results from a product finder query
    """
    model = Product
    template_name = 'admin/restocking/show_product_finder_results.html'
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
