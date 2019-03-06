"""
Views surrounding the creation of test data for the project

These functions are not 'forbidden' and can be ran multiple times!
"""

import random
import datetime

from django.shortcuts import HttpResponse

from restocking.models import Order, OrderItem, Product, User, Transaction, TransactionItem, RestockingList, RestockingListItem

def create_order_3000(request):
    """
    Create an order of 3000 items

    In practice, an order of 3000 is not likely, but this is to simply test how
    the worst case scenario works.
    """
    products = list(Product.objects.all())
    order_items = []
    order = Order(delivery_date='2019-01-02', order_delivered=True, order_processed=True)
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

    return HttpResponse('Done')

def create_transaction_200(request):
    """
    Create 200 transactions

    Adapted from test.
    """

    products = list(Product.objects.all())
    transaction_items = []
    transactions = []

    for i in range(200):
        transaction = Transaction(user=User.objects.get(id=1))
        transaction.save()
        transactions.append(transaction)
        for j in range(random.randint(1, 3)):
            products = list(Product.objects.filter(floor_quantity__gt=0))
            rnd_quantity = 1
            rnd_product = random.randrange(0, len(products))
            products[rnd_product].floor_quantity -= rnd_quantity
            products[rnd_product].save()
            transaction_items.append(TransactionItem(
                quantity=rnd_quantity,
                product=products[rnd_product],
                transaction=transaction,
            ))

    for item in transaction_items:
        item.save()

    return HttpResponse('Done')

def generate_restocking_list(request):
    restocking_list = RestockingList.objects.latest()
    transaction_items = []

    for i in Transaction.objects.filter(
            time__lt=datetime.datetime.now(),
            time__gt=restocking_list.time,
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
    
    return HttpResponse('Done')