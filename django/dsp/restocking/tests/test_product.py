"""
Tests surrounding the valid creation of products.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from restocking.models import *

class TestProduct(TestCase):
    """Validation tests for creating products"""

    def test_create_valid_product(self):
        """Create a valid product"""
        product_name = "Swift Iris"
        size = Size.SIZE_4_5
        colour = "Red"
        price = 47.00
        product_type = ProductType.SHOE
        product_code = "A"
        department = Department.LADIES

        product = Product(
            name=product_name,
            size=size,
            colour=colour,
            price=price,
            product_type=product_type,
            product_code=product_code,
            department=department,
            )
        
        product.save()

    def test_create_invalid_product_long_name(self):
        """Create an invalid product where its name is too long"""
        product_name = "1234567890123456789098765432112345678900987654322123"
        size = Size.SIZE_4_5
        colour = "Red"
        price = 47.00
        product_type = ProductType.SHOE
        product_code = "A"
        department = Department.LADIES

        product = Product(
            name=product_name,
            size=size,
            colour=colour,
            price=price,
            product_type=product_type,
            product_code=product_code,
            department=department,
            )

        with self.assertRaises(ValidationError):
            product.clean()

    def test_create_invalid_product_no_name(self):
        """Create an invalid product with no name"""
        size = Size.SIZE_4_5
        colour = "Red"
        price = 47.00
        product_type = ProductType.SHOE
        product_code = "A"
        department = Department.LADIES

        product = Product(
            size=size,
            colour=colour,
            price=price,
            product_type=product_type,
            product_code=product_code,
            department=department,
            )

        with self.assertRaises(ValidationError):
            product.clean()

    def test_create_invalid_product_blank_name(self):
        """Create an invalid product with a blank name"""
        product_name = ""
        size = Size.SIZE_4_5
        colour = "Red"
        price = 47.00
        product_type = ProductType.SHOE
        product_code = "A"
        department = Department.LADIES

        product = Product(
            name=product_name,
            size=size,
            colour=colour,
            price=price,
            product_type=product_type,
            product_code=product_code,
            department=department,
            )

        with self.assertRaises(ValidationError):
            product.clean()

    def test_create_invalid_product_code_lower_case(self):
        """Create an invalid product with a lower case code"""
        product_name = "Swift Iris"
        size = Size.SIZE_4_5
        colour = "Red"
        price = 47.00
        product_type = ProductType.SHOE
        product_code = "a"
        department = Department.LADIES

        product = Product(
            name=product_name,
            size=size,
            colour=colour,
            price=price,
            product_type=product_type,
            product_code=product_code,
            department=department,
            )

        with self.assertRaises(ValidationError):
            product.clean()

    def test_create_invalid_product_code_lengthly(self):
        """Create an invalid product with a lengthly code"""
        product_name = "Swift Iris"
        size = Size.SIZE_4_5
        colour = "Red"
        price = 47.00
        product_type = ProductType.SHOE
        product_code = "asdfghjk"
        department = Department.LADIES

        product = Product(
            name=product_name,
            size=size,
            colour=colour,
            price=price,
            product_type=product_type,
            product_code=product_code,
            department=department,
            )

        with self.assertRaises(ValidationError):
            product.clean()

    def test_create_invalid_price_three_dp(self):
        """Create an invalid product where the price has 3dp"""
        product_name = "Swift Iris"
        size = Size.SIZE_4_5
        colour = "Red"
        price = 47.123
        product_type = ProductType.SHOE
        product_code = "A"
        department = Department.LADIES

        product = Product(
            name=product_name,
            size=size,
            colour=colour,
            price=price,
            product_type=product_type,
            product_code=product_code,
            department=department,
            )

        with self.assertRaises(ValidationError):
            product.clean()

    def test_create_invalid_price_higher_than_999(self):
        """Create an invalid product where its price is higher than 999"""
        product_name = "Swift Iris"
        size = Size.SIZE_4_5
        colour = "Red"
        price = 1001
        product_type = ProductType.SHOE
        product_code = "A"
        department = Department.LADIES

        product = Product(
            name=product_name,
            size=size,
            colour=colour,
            price=price,
            product_type=product_type,
            product_code=product_code,
            department=department,
            )

        with self.assertRaises(ValidationError):
            product.clean()