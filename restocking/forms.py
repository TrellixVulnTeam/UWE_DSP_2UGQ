"""
Forms for administration or management purposes
"""
from django import forms
from .models import Size, Fitting, ProductType, Department

class ProductFinderForm(forms.Form):
    """
    Form used by admin for finding products.
    """
    name = forms.CharField(label='Product Name', required=False)
    filter_name = forms.BooleanField(label='Ignore Field', required=False)

    size = forms.ChoiceField(label='Size', choices=Size.choices)
    filter_size = forms.BooleanField(label='Ignore Field', required=False)

    colour = forms.CharField(label='Colour', required=False)
    filter_colour = forms.BooleanField(label='Ignore Field', required=False)

    fitting = forms.ChoiceField(label='Fitting', choices=Fitting.choices, required=False)
    filter_fitting = forms.BooleanField(label='Ignore Field', required=False)

    price = forms.CharField(label='Price', required=False)
    filter_price = forms.BooleanField(label='Ignore Field', required=False)

    sale = forms.BooleanField(label='Is on Sale', required=False)
    filter_sale = forms.BooleanField(label='Ignore Field', required=False)

    product_type = forms.ChoiceField(label='Product Type', choices=ProductType.choices, required=False)
    filter_product_type = forms.BooleanField(label='Ignore Field', required=False)

    product_code = forms.CharField(label='Product Code', required=False)
    filter_product_code = forms.BooleanField(label='Ignore Field', required=False)

    department = forms.ChoiceField(label='Department', choices=Department.choices, required=False)
    filter_department = forms.BooleanField(label='Ignore Field', required=False)
