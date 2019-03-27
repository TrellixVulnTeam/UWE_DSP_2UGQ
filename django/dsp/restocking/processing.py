from restocking.models import Product, RestockingListItem, Transaction, TransactionItem, RestockingList, Order, OrderItem, ProductType

import django.utils.timezone as timezone
import datetime

class RecommendProcessing():
    """
    Processing related to recommending a product
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
        ).exclude(id=item.product.id)

    def check_ignore_fitting(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_colour(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_fitting_colour(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            size=item.product.size,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_name(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_name_fitting(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_name_colour(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_name_fitting_colour(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            size=item.product.size,
            department=item.product.department,
            floor_quantity=0,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_out(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_out_fitting(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_out_colour(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_out_fitting_colour(self, item):
        return Product.objects.filter(
            name=item.product.name,
            product_code=item.product.product_code,
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_out_name(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_out_name_fitting(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            colour=item.product.colour,
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_out_name_colour(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            size=item.product.size,
            fitting=item.product.fitting,
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_out_name_fitting_colour(self, item):
        return Product.objects.filter(
            product_code=item.product.product_code,
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_code(self, item):
        return Product.objects.filter(
            size=item.product.size,
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def check_ignore_size(self, item):
        return Product.objects.filter(
            department=item.product.department,
            stock_quantity__gt=0
        ).exclude(id=item.product.id)

    def recommend(self, item):
        if hasattr(item, 'product'):
            print('isItem')
            print(item.id)
        else:
            item = RestockingListItem.objects.get(id=item)
        candidates = self.check(item)
        if not candidates:
            #print('check_ignore_fitting')
            candidates = self.check_ignore_fitting(item)
            if not candidates:
                #print('check_ignore_colour')
                candidates = self.check_ignore_colour(item)
                if not candidates:
                    #print('check_ignore_fitting_colour')
                    candidates = self.check_ignore_fitting_colour(item)
                    if not candidates:
                        #print('check_ignore_name')
                        candidates = self.check_ignore_name(item)
                        if not candidates:
                            #print('check_ignore_name_fitting')
                            candidates = self.check_ignore_name_fitting(item)
                            if not candidates:
                                #print('check_ignore_name_colour')
                                candidates = self.check_ignore_name_colour(item)
                                if not candidates:
                                    #print('check_ignore_name_fitting_colour')
                                    candidates = self.check_ignore_name_fitting_colour(item)
                                    if not candidates:
                                        #print('check_ignore_out')
                                        candidates = self.check_ignore_out(item)
                                        if not candidates:
                                            #print('check_ignore_out_fitting')
                                            candidates = self.check_ignore_out_fitting(item)
                                            if not candidates:
                                                #print('check_ignore_out_colour')
                                                candidates = self.check_ignore_out_colour(item)
                                                if not candidates:
                                                    #print('check_ignore_out_fitting_colour')
                                                    candidates = self.check_ignore_out_fitting_colour(item)
                                                    if not candidates:
                                                        #print('check_ignore_out_name')
                                                        candidates = self.check_ignore_out_name(item)
                                                        if not candidates:
                                                            #print('check_ignore_out_name_fitting')
                                                            candidates = self.check_ignore_out_name_fitting(item)
                                                            if not candidates:
                                                                #print('check_ignore_out_name_colour')
                                                                candidates = self.check_ignore_out_name_colour(item)
                                                                if not candidates:
                                                                    #print('check_ignore_out_name_fitting_colour')
                                                                    candidates = self.check_ignore_out_name_fitting_colour(item)
                                                                    if not candidates:
                                                                        #print('check_ignore_code')
                                                                        candidates = self.check_ignore_code(item)
                                                                        if not candidates:
                                                                            #print('check_ignore_size')
                                                                            candidates = self.check_ignore_size(item)

        return candidates        

class RestockingListProcessing:
    def create_restocking_list(self):
        restocking_list = RestockingList.objects.latest('id')
        transaction_items = []

        for i in Transaction.objects.filter(
                datetime__lt=timezone.now(),
                datetime__gt=restocking_list.datetime
        ).iterator():
            transaction_items.append(TransactionItem.objects.filter(transaction=i))


        current_list = RestockingList.objects.create()
        #Create a list of transaction items that will fall within the restocking list
        restocking_list_items = transaction_items[0]
        transaction_items.pop(0)
        for i in transaction_items:
            restocking_list_items = restocking_list_items | i

        for item in list(restocking_list_items):
            if item.product.stock_quantity != 0:
                RestockingListItem.objects.create(
                    quantity=item.quantity,
                    product=item.product,
                    restocking_list=current_list
                )
            else:
                print('had to go with a recommended product')
                recommended = list(RecommendProcessing().recommend(RestockingListItem(product=item.product)))[0]
                RestockingListItem.objects.create(
                    quantity=item.quantity,
                    product=recommended,
                    restocking_list=current_list
                )
    
class OrderProcessing:
    def is_spring(self):
        return (datetime.date(timezone.now().date().year, 3, 1) <= timezone.now().date() and timezone.now().date() >= datetime.date(timezone.now().date().year, 5, 31))
    
    def is_summer(self):
        return datetime.date(timezone.now().date().year, 6, 1) <= timezone.now().date() <= datetime.date(timezone.now().date().year, 8, 31)
    
    def is_autumn(self):
        return datetime.date(timezone.now().date().year, 9, 1) <= timezone.now().date() <= datetime.date(timezone.now().date().year(), 11, 30)

    def is_winter(self):
        if (timezone.now().date().year() + 1) % 4 == 0:#leap year
            return datetime.date(timezone.now().date().year, 12, 1) <= timezone.now().date() <= datetime.date(timezone.now().date().year + 1, 2, 29)
        else:
            return datetime.date(timezone.now().date().year, 12, 1) <= timezone.now().date() <= datetime.date(timezone.now().date().year + 1, 2, 28)

    def get_quantity_multiplier(self, quantity):
        if quantity >= 5:
            return 1.5
        elif quantity >= 10:
            return 1
        else:
            return 1

    def order_different_colour(self, product, order):
        for i in Product.objects.filter(
            name=product.name,
            size=product.size,
            fitting=product.fitting
        ).iterator():
            OrderItem.objects.create(
                product=i,
                quantity=1,
                order=order
            )

    def create_order_item(self, item, order):
        if(item.quantity > 15):
            item.quantity = 15
        
        OrderItem.objects.create(
            product=item.product,
            quantity=round((item.quantity + item.quantity_from_stock_room) * self.get_quantity_multiplier(item.quantity)),
            order=order
        )

        if(item.quantity >= 10):
            self.order_different_colour(item.product, order)


    def create_order(self):
        if Order.objects.filter(delivery_date=timezone.now().date()).exists():
            return None

        transaction_items = []

        for i in Transaction.objects.filter(date=timezone.now().date()).iterator():
            transaction_items.append(TransactionItem.objects.filter(transaction=i))

        order_items = transaction_items[0]
        transaction_items.pop(0)
        for i in transaction_items:
            order_items = order_items | i
        #Sets the order as delivered for the purposes of this project.
        order = Order.objects.create(order_processed=True, order_delivered=True, delivery_date=timezone.now().date())

        for item in list(order_items):
            #If item is already on the list, just add it to its quantity.
            if OrderItem.objects.filter(order=order, product__id=item.product.id).exists():
                p = OrderItem.objects.get(order=order, product__id=item.product.id)
                p.quantity = p.quantity + item.quantity + item.quantity_from_stock_room
                p.save()
            else:
                if self.is_spring() or self.is_autumn():
                    self.create_order_item(item, order)

                elif self.is_summer():
                    if item.product.product_type != ProductType.SLIPPER:
                        self.create_order_item(item, order)

                elif self.is_winter:
                    if item.product.product_type != ProductType.SANDAL:
                        self.create_order_item(item, order)

        return OrderItem.objects.filter(order=order)