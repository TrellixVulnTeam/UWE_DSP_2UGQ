from django.test import TestCase
from restocking.models import Product, Fitting, Department, ProductType, Size
import random
import os
import json 

class TestProductData(TestCase):
    def setUp(self):
        """Creates random data from a file"""
        _colour_pop_chance = 50
        _fitting_pop_chance = 75
        products = []
        def randint_x(n_1, n_2):
            """Returns a random number within the given range (exclusive)"""
            return random.randint(n_1, n_2-1)

        self.path = os.getcwd()
        with open(self.path + '/restocking/product_metadata.json') as data_file:
            self.product_md = json.load(data_file)

        name_list = []#list to prevent duplicate names
        for department in self.product_md:
            for code in self.product_md[department]['codes']:
                for shoe in range(self.product_md[department]['codes'][code]['quantity']):
                    #Name
                    duplicate = True
                    while duplicate:
                        primary_name = self.product_md[department]['codes'][code]['names'][randint_x(0, len(self.product_md[department]['codes'][code]['names']))]
                        secondary_name = self.product_md[department]['secondary'][randint_x(0, len(self.product_md[department]['secondary']))]
                        name = primary_name+" "+secondary_name
                        if name not in name_list:
                            name_list.append(name)
                            duplicate = False
                    #Size
                    sizes = []
                    if department == 'childrens':
                        for size in range(0, len(self.product_md[department]['codes'][code]['sizes'])):
                            sizes.append(self.product_md[department]['codes'][code]['sizes'][size])
                    else:
                        for size in range(0, len(self.product_md[department]['codes'][code]['sizes']), random.randint(1, 2)):
                            sizes.append(self.product_md[department]['codes'][code]['sizes'][size])
                    #Fitting
                    fittings = list(self.product_md[department]['codes'][code]['fittings'])
                    if department == 'childrens':
                        if self.product_md[department]['codes'][code]['type'] == 'shoe' and random.randint(0, 1) == 1:
                            fittings.pop()
                            fittings.pop()
                    else:
                        for x in range(0, len(fittings)-1):
                            if random.randint(0, 100) <= _fitting_pop_chance:
                                fittings.pop()
                    #Colour
                    colours = list(self.product_md[department]['codes'][code]['colours'])
                    for x in range(len(colours)-1):
                        if random.randint(0, 100) <= _colour_pop_chance:
                            colours.pop()
                    #Price
                    price = self.product_md[department]['codes'][code]['prices'][randint_x(0, len(self.product_md[department]['codes'][code]['prices']))]
                    product_type = self.product_md[department]['codes'][code]['type']
                    product_code = code
                    department = department

                    for size in sizes:
                        for fitting in fittings:
                            for colour in colours:
                                Product.objects.create(
                                    name=name,
                                    size=size,
                                    fitting=fitting,
                                    colour=colour,
                                    price=price,
                                    product_type=product_type,
                                    product_code=product_code,
                                    department=department
                                )

    def test_adding_product_quantities(self):
        """
        Test assigning random(ish) quantities to each product.
        """

        path = os.getcwd()
        with open(self.path + '/restocking/data/initial_product_levels.json') as data_file:
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
            print quantity
            product.stock_quantity = quantity + random.randint((quantity/2 * -1), (quantity/2))
            print product.__str__() + ' ' + str(product.stock_quantity)

        
