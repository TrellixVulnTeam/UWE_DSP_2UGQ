from django.db import models

# Create your models here.

import datetime

from django.db import models
from djchoices import ChoiceItem, DjangoChoices
import django.core.validators as validator

class Fitting(DjangoChoices):
    D = ChoiceItem('d', 'D')
    E = ChoiceItem('e', 'E')
    F = ChoiceItem('f', 'F')
    G = ChoiceItem('g', 'G')
    H = ChoiceItem('h', 'H')
    WIDE = ChoiceItem('wide', 'Wide')
    STANDARD = ChoiceItem('standard', 'Standard')

class Department(DjangoChoices):
    LADIES = ChoiceItem('ladies', 'Ladies')
    MENS = ChoiceItem('mens', 'Mens')
    CHILDRENS = ChoiceItem('childrens', 'Childrens')

class ProductType(DjangoChoices):
    SHOE = ChoiceItem('shoe', 'Shoe')
    BOOT = ChoiceItem('boot', 'Boot')
    SANDAL = ChoiceItem('sandal', 'Sandal')
    SLIPPER = ChoiceItem('slipper', 'Slipper')

class Size(DjangoChoices):
    SIZE_1 = ChoiceItem(1, 1)
    SIZE_1_5 = ChoiceItem(1.5, 1.5)
    SIZE_2 = ChoiceItem(2, 2)
    SIZE_2_5 = ChoiceItem(2.5, 2.5)
    SIZE_3 = ChoiceItem(3, 3)
    SIZE_3_5 = ChoiceItem(3.5, 3.5)
    SIZE_4 = ChoiceItem(4, 4)
    SIZE_4_5 = ChoiceItem(4.5, 4.5)
    SIZE_5 = ChoiceItem(5, 5)
    SIZE_5_5 = ChoiceItem(5.5, 5.5)
    SIZE_6 = ChoiceItem(6, 6)
    SIZE_6_5 = ChoiceItem(6.5, 6.5)
    SIZE_7 = ChoiceItem(7, 7)
    SIZE_7_5 = ChoiceItem(7.5, 7.5)
    SIZE_8 = ChoiceItem(8, 8)
    SIZE_8_5 = ChoiceItem(8.5, 8.5)
    SIZE_9 = ChoiceItem(9, 9)
    SIZE_9_5 = ChoiceItem(9.5, 9.5)
    SIZE_10 = ChoiceItem(10, 10)
    SIZE_10_5 = ChoiceItem(10.5, 10.5)
    SIZE_11 = ChoiceItem(11, 11)
    SIZE_11_5 = ChoiceItem(11.5, 11.5)
    SIZE_12 = ChoiceItem(12, 12)
    SIZE_12_5 = ChoiceItem(12.5, 12.5)
    SIZE_13 = ChoiceItem(13, 13)
    SIZE_13_5 = ChoiceItem(13.5, 13.5)
    SIZE_14 = ChoiceItem(14, 14)

# Create your models here.
class Product(models.Model):
    codes = validator.RegexValidator(r'[A-Z]', 'Only capital alphabet characters are allowed.')

    def __str__(self):
        return self.name + " size " + str(self.size) + " " + self.fitting + " in " + self.colour

    name = models.CharField(max_length=50)
    size = models.DecimalField(max_digits=4, decimal_places=1, choices=Size.choices)
    colour = models.CharField(max_length=20)
    fitting = models.CharField(max_length=8, choices=Fitting.choices, default=Fitting.STANDARD)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sale = models.BooleanField(default=False)
    product_type = models.CharField(max_length=10, choices=ProductType.choices)
    product_code = models.CharField(max_length=10, validators=[codes])
    department = models.CharField(max_length=10, choices=Department.choices)
    floor_quantity = models.IntegerField(default=0)
    stock_quantity = models.IntegerField(default=0)

class Order(models.Model):
    order_processed = models.BooleanField(default=False)
    order_delivered = models.BooleanField(default=False)
    delivery_date = models.DateField(null=True, blank=True, unique=True)
    delivery_processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.delivery_date)

class OrderItem(models.Model):
    quantity = models.IntegerField(default=1, validators=[validator.MinValueValidator(1, "There is a value that is less than 0")])
    processed = models.IntegerField(default=0, validators=[validator.MinValueValidator(0, "There is a value that is less than 0")])
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE)
    added = models.BooleanField(default=False)

    def __str__(self):
        return (str(self.product) + ' (' + str(self.processed) + '/' + str(self.quantity)) + ')'

class User(models.Model):
    password = models.CharField(max_length=12)

    def __str__(self):
        return str(self.id)

class Transaction(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    def __str__(self):
        return '(' + str(self.id) + ') (' + str(self.date) + ') (' + str(self.time.strftime('%H:%M:%S')) +')'

class TransactionItem(models.Model):
    quantity = models.IntegerField(default=1, validators=[validator.MinValueValidator(1, "There is a value that is less than 1")])
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.transaction.id) + ' ' + str(self.product) + ' (' + str(self.quantity) + ')'

class RestockingList(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return str(self.date) + ' ' + str(self.time.strftime('%H:%M:%S'))

class RestockingListItem(models.Model):
    quantity = models.IntegerField(default=1, validators=[validator.MinValueValidator(1, "There is a value that is less than 1")])
    processed = models.IntegerField(default=0, validators=[validator.MinValueValidator(0, "There is a value that is less than 0")])
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added = models.BooleanField(default=False)
    restocking_list = models.ForeignKey('RestockingList', related_name='restocking_items', on_delete=models.CASCADE)


