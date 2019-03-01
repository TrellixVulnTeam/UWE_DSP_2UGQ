"""
All of the navigation views for the admin pages.
"""
from django.shortcuts import redirect
from django.views import generic
from restocking.forms import ProductFinderForm

class IndexView(generic.ListView):
    """
    Home page for admin for application
    """
    template_name = 'admin/restocking/index.html'

    def get_queryset(self):
        return None

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
