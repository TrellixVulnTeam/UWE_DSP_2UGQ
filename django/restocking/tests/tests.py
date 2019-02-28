"""
General Tests
Most Processing logic is done here first before done in the application
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# pylint: disable=attribute-defined-outside-init
# pylint: disable=line-too-long
# pylint: disable=too-many-instance-attributes

import nfc
import json
import os
import random
from django.core.exceptions import ValidationError
from django.test import TestCase
from restocking.models import Product, RestockingList, RestockingListItem, Fitting, Department, ProductType, Size


# Create your tests here.
class CreatingProductsTestCase(TestCase):
    """Validation tests for creating products"""

    def test_create_valid_product(self):
        """Create a valid product"""
        self.product_name = "Swift Iris"
        self.size = Size.SIZE_4_5
        self.colour = "Red"
        self.price = 47.00
        self.product_type = ProductType.SHOE
        self.product_code = "A"
        self.department = Department.LADIES

        self.product = Product(
            name=self.product_name,
            size=self.size,
            colour=self.colour,
            price=self.price,
            product_type=self.product_type,
            product_code=self.product_code,
            department=self.department,
            )
        self.full_clean()
        self.assertFalse(self.product is None)

    def test_create_invalid_product_long_name(self):
        """Create an invalid product where its name is too long"""
        self.product_name = "1234567890123456789098765432112345678900987654322123"
        self.size = Size.SIZE_4_5
        self.colour = "Red"
        self.price = 47.00
        self.product_type = ProductType.SHOE
        self.product_code = "A"
        self.department = Department.LADIES

        self.product = Product(
            name=self.product_name,
            size=self.size,
            colour=self.colour,
            price=self.price,
            product_type=self.product_type,
            product_code=self.product_code,
            department=self.department,
            )

        with self.assertRaises(ValidationError):
            self.full_clean()

    def test_create_invalid_product_no_name(self):
        """Create an invalid product with no name"""
        self.size = Size.SIZE_4_5
        self.colour = "Red"
        self.price = 47.00
        self.product_type = ProductType.SHOE
        self.product_code = "A"
        self.department = Department.LADIES

        self.product = Product(
            size=self.size,
            colour=self.colour,
            price=self.price,
            product_type=self.product_type,
            product_code=self.product_code,
            department=self.department,
            )

        with self.assertRaises(ValidationError):
            self.full_clean()

    def test_create_invalid_product_blank_name(self):
        """Create an invalid product with a blank name"""
        self.product_name = ""
        self.size = Size.SIZE_4_5
        self.colour = "Red"
        self.price = 47.00
        self.product_type = ProductType.SHOE
        self.product_code = "A"
        self.department = Department.LADIES

        self.product = Product(
            name=self.product_name,
            size=self.size,
            colour=self.colour,
            price=self.price,
            product_type=self.product_type,
            product_code=self.product_code,
            department=self.department,
            )

        with self.assertRaises(ValidationError):
            self.full_clean()

    def test_create_invalid_product_code_lower_case(self):
        """Create an invalid product with a lower case code"""
        self.product_name = "Swift Iris"
        self.size = Size.SIZE_4_5
        self.colour = "Red"
        self.price = 47.00
        self.product_type = ProductType.SHOE
        self.product_code = "a"
        self.department = Department.LADIES

        self.product = Product(
            name=self.product_name,
            size=self.size,
            colour=self.colour,
            price=self.price,
            product_type=self.product_type,
            product_code=self.product_code,
            department=self.department,
            )

        with self.assertRaises(ValidationError):
            self.full_clean()

    def test_create_invalid_product_code_lengthly(self):
        """Create an invalid product with a lengthly code"""
        self.product_name = "Swift Iris"
        self.size = Size.SIZE_4_5
        self.colour = "Red"
        self.price = 47.00
        self.product_type = ProductType.SHOE
        self.product_code = "asdfghjk"
        self.department = Department.LADIES

        self.product = Product(
            name=self.product_name,
            size=self.size,
            colour=self.colour,
            price=self.price,
            product_type=self.product_type,
            product_code=self.product_code,
            department=self.department,
            )

        with self.assertRaises(ValidationError):
            self.full_clean()

    def test_create_invalid_price_three_dp(self):
        """Create an invalid product where the price has 3dp"""
        self.product_name = "Swift Iris"
        self.size = Size.SIZE_4_5
        self.colour = "Red"
        self.price = 47.123
        self.product_type = ProductType.SHOE
        self.product_code = "A"
        self.department = Department.LADIES

        self.product = Product(
            name=self.product_name,
            size=self.size,
            colour=self.colour,
            price=self.price,
            product_type=self.product_type,
            product_code=self.product_code,
            department=self.department,
            )

        with self.assertRaises(ValidationError):
            self.full_clean()

    def test_create_invalid_price_higher_than_999(self):
        """Create an invalid product where its price is higher than 999"""
        self.product_name = "Swift Iris"
        self.size = Size.SIZE_4_5
        self.colour = "Red"
        self.price = 1001
        self.product_type = ProductType.SHOE
        self.product_code = "A"
        self.department = Department.LADIES

        self.product = Product(
            name=self.product_name,
            size=self.size,
            colour=self.colour,
            price=self.price,
            product_type=self.product_type,
            product_code=self.product_code,
            department=self.department,
            )

        with self.assertRaises(ValidationError):
            self.full_clean()

class CreateResockingListItemTestCase(TestCase):
    """Validation tests for creating restocking lists"""
    def test_create_list_of_one_item_with_0_quantity(self):
        """Create an invalid list where an item has 0 quantity"""
        self.product_name = "Swift Iris"
        self.size = Size.SIZE_4_5
        self.colour = "Red"
        self.price = 47.00
        self.product_type = ProductType.SHOE
        self.product_code = "A"
        self.department = Department.LADIES

        self.product = Product(
            name=self.product_name,
            size=self.size,
            colour=self.colour,
            price=self.price,
            product_type=self.product_type,
            product_code=self.product_code,
            department=self.department,
            )
        self.list = RestockingList()

        self.restocking_list_item = RestockingListItem(
            product=self.product,
            restocking_list=self.list,
            quantity=0
        )

        with self.assertRaises(ValidationError):
            self.restocking_list_item.full_clean()

class CreatingTestDataTestCase(TestCase):
    """Test for creating test data"""
    def disabletest_create_product_data(self):
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
                                product = Product(
                                    name=name,
                                    size=size,
                                    fitting=fitting,
                                    colour=colour,
                                    price=price,
                                    product_type=product_type,
                                    product_code=product_code,
                                    department=department
                                )
                                save()
                                products.append(product)
            print "made products"
        for x in products:
            print x
        print len(products)