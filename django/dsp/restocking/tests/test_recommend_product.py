"""
Test for recommending a product if a needed product is not in stock.

The factors that affect a product being recommended are...
-A style missing from the shelf when the system last checked - High
-A style similar to the style missing from the shelf when the system last checked
in the event of the same style not being in stock
-A style that is not currently out
-A style with high sales figures
-A style that has a different colour
"""

import random
import os
import json

from django.utils import timezone
from django.test import TestCase
from django.db.models import Q
from restocking.models import RestockingList, Product, User, Transaction, RestockingList, RestockingListItem, TransactionItem

class TestRecommendProduct(TestCase):
    """
    Test for recommending a product if a needed product is not in stock
    """

    def check(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        )

    def check_ignore_fitting(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        )

    def check_ignore_colour(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        )

    def check_ignore_fitting_colour(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            size=item.product.size,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        )

    def check_ignore_name(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        )

    def check_ignore_name_fitting(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        )

    def check_ignore_name_colour(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        )

    def check_ignore_name_fitting_colour(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            size=item.product.size,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        )

    def check_ignore_out(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            stock_quantity__gt=0
        )
    
    def check_ignore_out_fitting(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        )
    
    def check_ignore_out_colour(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            stock_quantity__gt=0
        )
    
    def check_ignore_out_fitting_colour(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        )
    
    def check_ignore_out_name(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            stock_quantity__gt=0
        )

    def check_ignore_out_name_fitting(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        )

    def check_ignore_out_name_colour(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            stock_quantity__gt=0
        )

    def check_ignore_out_name_fitting_colour(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        )

    def check_ignore_code(self, item):
        return Product.objects.filter(
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        )

    def check_ignore_size(self, item):
        return Product.objects.filter(
            department=item.product.department,
            stock_quantity__gt=0
        ) 

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

        restocking_list = RestockingList(time=str(timezone.now()))
        restocking_list.save()
        transaction_items = []

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

        #Randomly drop product quantities
        quantity_pop_chance = 20
        for item in RestockingListItem.objects.all().iterator():
            if random.randint(0, 100) <= quantity_pop_chance:
                product = Product.objects.get(id=item.product.id)
                product.stock_quantity = 0
                product.save()
                if random.randint(0, 100) <= quantity_pop_chance:
                    products = self.check_ignore_fitting(item)
                    for to_remove in products.iterator():
                        to_remove.stock_quantity = 0
                        to_remove.save()

                    if random.randint(0, 100) <= quantity_pop_chance:
                        products = self.check_ignore_colour(item)
                        for to_remove in products.iterator():
                            to_remove.stock_quantity = 0
                            to_remove.save()

                        if random.randint(0, 100) <= quantity_pop_chance:
                            products = self.check_ignore_out(item)
                            for to_remove in products.iterator():
                                to_remove.stock_quantity = 0
                                to_remove.save()

                            if random.randint(0, 100) <= quantity_pop_chance:
                                products = self.check_ignore_code(item)
                                for to_remove in products.iterator():
                                    to_remove.stock_quantity = 0
                                    to_remove.save()

                                if random.randint(0, 100) <= quantity_pop_chance:
                                    products = self.check_ignore_size(item)
                                    for to_remove in products.iterator():
                                        to_remove.stock_quantity = 0
                                        to_remove.save()

    def test_recommend_product(self):
        for item in RestockingListItem.objects.all().iterator():
            if item.product.stock_quantity == 0:
                """
                To find the perfect replacement, we need a product that...
                -Is the same code 3
                -Is the same colour 5
                -Is the same size 2
                -Is the same fitting 6
                -Is the same department 1 - We can't remove this
                -Is not out 4

                This is not always possible, so we can remove attributes until we find something
                that is 'good enough'
                """
                
                candidates = self.check(item)

                print('To replace ' + str(item.product) + ', we have...')

                if not candidates:
                    print('...absolutely nothing! Filtering fittings...')
                    candidates = self.check_ignore_fitting(item)
                    if not candidates:
                        print('...still nothing! Filtering colours...')
                        candidates = self.check_ignore_colour(item)
                        if not candidates:
                            print('...still nothing! Filtering fittings and colours...')
                            candidates = self.check_ignore_fitting_colour(item)
                            if not candidates:
                                print('...still nothing! Filtering name...')
                                candidates = self.check_ignore_name(item)
                                if not candidates:
                                    print('...still nothing! Filtering name and fitting...')
                                    candidates = self.check_ignore_name_fitting(item)
                                    if not candidates:
                                        print('...still nothing! Filtering name and colour...')
                                        candidates = self.check_ignore_name_colour(item)
                                        if not candidates:
                                            print('...still nothing! Filtering name, fitting and colour...')
                                            candidates = self.check_ignore_name_fitting_colour(item)
                                            if not candidates:
                                                print('...still nothing! Filtering out...')
                                                candidates = self.check_ignore_out(item)
                                                if not candidates:
                                                    print('...still nothing! Filtering out and fitting...')
                                                    candidates = self.check_ignore_out_fitting(item)
                                                    if not candidates:
                                                        print('...still nothing! Filtering out and colour...')
                                                        candidates = self.check_ignore_out_colour(item)
                                                        if not candidates:
                                                            print('...still nothing! Filtering out, fitting and colour...')
                                                            candidates = self.check_ignore_out_fitting_colour(item)
                                                            if not candidates:
                                                                print('...still nothing! Filtering out and name...')
                                                                candidates = self.check_ignore_out_name(item)
                                                                if not candidates:
                                                                    print('...still nothing! Filtering out, name and fitting...')
                                                                    candidates = self.check_ignore_out_name_fitting(item)
                                                                    if not candidates:
                                                                        print('...still nothing! Filtering out, name and colour...')
                                                                        candidates = self.check_ignore_out_name_colour(item)
                                                                        if not candidates:
                                                                            print('...still nothing! Filtering out, name, fitting and colour...')
                                                                            candidates = self.check_ignore_out_name_fitting_colour(item)
                                                                            if not candidates:
                                                                                candidates = self.check_ignore_code(item)
                                                                                #It shouldn't really get here...
                                                                                raise Exception('Got to ignore code')
                                                                                if not candidates:
                                                                                    candidates = self.check_ignore_size(item)
                                                                                    print('got to ignore size')
                             
                for candidate in candidates.iterator():
                    print(candidate)
                
