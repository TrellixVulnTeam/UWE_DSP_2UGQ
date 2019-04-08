"""
Tests surrounding the valid creation of transactions.
"""

import os
import random
import json

from django.test import TestCase
from restocking.models import *

class TestTransaction(TestCase):
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
    
        path = os.getcwd()
        with open(path + '\\restocking\\data\\initial_product_levels.json') as data_file:
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
            product.stock_quantity = quantity + random.randint((round(quantity/2) * -1), (round(quantity/2)))
            product.save()
        print('setup')

    def test_create_transaction_600(self):
        """Test for creating 600 transactions"""
        transaction_items = []
        transactions = []

        user = User(password='1234')
        user.save()

        for i in range(600):
            products = list(Product.objects.filter(stock_quantity__gt=0))
            transaction = Transaction(user=user)
            transaction.save()
            transactions.append(transaction)
            for j in range(random.randint(1, 3)):
                rnd_quantity = random.randint(1, 3)
                rnd_product = random.randrange(0, len(products))
                #print(products[rnd_product].stock_quantity)
                while rnd_quantity > products[rnd_product].stock_quantity:
                    rnd_quantity = random.randint(1, 3)
                products[rnd_product].stock_quantity -= rnd_quantity
                #print('\t ' + str(products[rnd_product].stock_quantity))
                transaction_items.append(TransactionItem(
                    quantity=rnd_quantity,
                    product=products[rnd_product],
                    transaction=transaction,
                ))


        for item in transaction_items:
            item.save()
            #print(item.transaction.time)

        self.assertEqual(len(transactions), 600)
