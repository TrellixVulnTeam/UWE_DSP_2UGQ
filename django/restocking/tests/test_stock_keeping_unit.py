from django.test import TestCase
from restocking.models import StockKeepingUnit
import os
import json

class TestStockKeepingUnit(TestCase):
    def setup(self):
        path = os.getcwd()
        with open(path + '/restocking/data/stock_keeping_units.json') as data_file:
            sku_data = json.load(data_file)

        for i in range (sku_data['department']['mens']['quantity']):
            StockKeepingUnit.objects.create()

        for i in range (sku_data['department']['ladies']['quantity']):
            StockKeepingUnit.objects.create()

        for i in range (sku_data['department']['childrens']['quantity']):
            StockKeepingUnit.objects.create()

    def test_populate_shop_floor(self):
        for sku in StockKeepingUnit.objects.all().iterator():
            for shelf_space in range(sku.product_limit):
                
        