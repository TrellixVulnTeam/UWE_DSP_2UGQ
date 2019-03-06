"""
Tests surrounding the valid creation of orders.
"""
import os
import random
import json

from django.test import TestCase
from django.core.exceptions import ValidationError
from restocking.models import *

class TestOrder(TestCase):
    """
    Tests surrounding the valid creation of orders.
    """
    def setUp(self):
        _colour_pop_chance = 50
        _fitting_pop_chance = 75
        def randint_x(n_1, n_2):
            """Returns a random number within the given range (exclusive)"""
            return random.randint(n_1, n_2-1)

        path = os.getcwd()
        with open(path + '\\restocking\\data\\product_metadata.json') as data_file:
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

    def test_create_order_of_100(self):
        """
        Test to create an order of 100 items
        """
        products = list(Product.objects.all())
        order_items = []
        order = Order(delivery_date='2019-01-01', order_delivered=True, order_processed=True)
        order.save()

        for i in range(100):
            rnd = random.randrange(0, len(products))
            order_items.append(OrderItem(
                quantity=random.randint(1, 4),
                product=products[rnd],
                order=order,
            ))
            products.pop(rnd)

        for item in order_items:
            item.save()

        self.assertEqual(len(order_items), 100)

    def test_create_order_of_3000(self):
        """
        Test to create an order of 3000 items
        """
        products = list(Product.objects.all())
        order_items = []
        order = Order(delivery_date='2019-01-01', order_delivered=True, order_processed=True)
        order.save()

        for i in range(3000):
            rnd = random.randrange(0, len(products))
            order_items.append(OrderItem(
                quantity=random.randint(1, 4),
                product=products[rnd],
                order=order,
            ))
            products.pop(rnd)

        for item in order_items:
            item.save()

        self.assertEqual(len(order_items), 3000)
        