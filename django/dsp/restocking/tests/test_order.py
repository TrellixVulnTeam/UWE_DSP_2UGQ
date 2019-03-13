"""
Tests surrounding the valid creation of orders.
"""
import os
import random
import json

from django.test import TestCase
from django.core.exceptions import ValidationError
from restocking.models import *
import django.utils.timezone as timezone

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
                sales = ProductSales.objects.get_or_create(
                    product=products[rnd_product],
                    date=timezone.now(),
                    defaults={'quantity': 0}
                )[0]
                sales.quantity = sales.quantity + rnd_quantity
                sales.save()
                #print('\t ' + str(products[rnd_product].stock_quantity) + ' ' + str(sales.quantity))
                transaction_items.append(TransactionItem(
                    quantity=rnd_quantity,
                    product=products[rnd_product],
                    transaction=transaction,
                ))


        for item in transaction_items:
            print(item)
            item.save()

    def silencetest_create_order_of_100(self):
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

    def silencetest_create_order_of_3000(self):
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

    def test_create_order_smart(self):
        """
        Test to create an order from the products sold
        """
        transaction_items = []

        for i in Transaction.objects.filter(
            date=timezone.now().date()
        ).iterator():
            transaction_items.append(TransactionItem.objects.filter(transaction=i))

        #Create a list of transaction items that will fall within the restocking list
        order_items = transaction_items[0]
        transaction_items.pop(0)
        for i in transaction_items:
            order_items = order_items | i
        order = Order()
        order.save()

        for item in list(order_items):
            OrderItem.objects.create(
                product=item.product,
                quantity=item.quantity,
                order=order
            )

        for item in OrderItem.objects.filter(order=order).iterator():
            print(item)