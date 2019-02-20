# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Product, Order, OrderItem, User, Transaction, TransactionItem, RestockingList, RestockingListItem, NfcUnit

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
admin.site.register(RestockingList)
admin.site.register(RestockingListItem)
admin.site.register(NfcUnit)
