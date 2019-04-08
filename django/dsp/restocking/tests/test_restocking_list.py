"""
Tests surrounding the valid creation of restocking lists.
"""

import os
import random
import json
from datetime import datetime

from django.utils import timezone

from django.test import TestCase
from restocking.models import *

class TestRestockingList(TestCase):
    def setUp(self):
        RestockingList.objects.create()

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
    
        products = list(Product.objects.all())
        transaction_items = []
        transactions = []

        user = User(password='1234')
        user.save()

        for i in range(600):
            transaction = Transaction(user=user)
            transaction.save()
            transactions.append(transaction)
            for j in range(random.randint(1, 3)):
                transaction_items.append(TransactionItem(
                    quantity=random.randint(1, 3),
                    product=products[random.randrange(0, len(products))],
                    transaction=transaction,
                ))

        for item in transaction_items:
            item.save()

    def test_restocking_list(self):
        restocking_list = RestockingList(time=str(timezone.now()))
        restocking_list.save()
        transaction_items = []

        #print(str(timezone.now()))
        #print(RestockingList.objects.get(id__exact=restocking_list.id-1).time)

        for i in Transaction.objects.filter(
                time__lt=timezone.now(),
                time__gt=RestockingList.objects.get(id__exact=restocking_list.id-1).time,
                date=restocking_list.date
        ).iterator():
            transaction_items.append(TransactionItem.objects.filter(transaction=i))

        #Create a list of transaction items that will fall within the restocking list
        restocking_list_items = transaction_items[0]
        transaction_items.pop(0)
        for i in transaction_items:
            restocking_list_items = restocking_list_items | i

        for item in list(restocking_list_items):
            RestockingListItem.objects.create(
                quantity=item.quantity,
                product=item.product,
                restocking_list=restocking_list
            )

        #for i in transaction_items:
            #print(i)
